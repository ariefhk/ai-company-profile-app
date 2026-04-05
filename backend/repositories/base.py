"""
Base repository with common async CRUD operations.

All repositories inherit from :class:`BaseRepository`, which provides
type-safe CRUD methods backed by a SQLAlchemy ``AsyncSession``.  The
session is expected to be managed externally (e.g. via a FastAPI
dependency) -- this class calls ``flush()`` but never ``commit()``,
so callers retain full control over transaction boundaries.
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import ColumnElement, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import QueryableAttribute, joinedload, selectinload

from core.exceptions import NotFoundException
from models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
IdType = TypeVar("IdType", int, str)


class BaseRepository(Generic[ModelType, IdType]):
    """Generic base repository providing standard async CRUD operations.

    Subclasses only need to bind the concrete model type::

        class UserRepository(BaseRepository[User, int]):
            def __init__(self, db: AsyncSession):
                super().__init__(User, db)

    Notes
    -----
    * All write helpers (``create``, ``update``, ``delete``) call
      ``flush()`` -- **not** ``commit()`` -- so that the caller (or an
      outer unit-of-work) decides when to commit the transaction.
    * ``find_*`` methods return ORM-mapped instances attached to the
      current session.  Detach or expire them explicitly if they must
      outlive the session.
    """

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model: Any = model
        self.db = db

    # --- Read ---
    async def find_by_id(self, id: IdType) -> ModelType | None:
        """Return a single record by primary key, or ``None``."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def find_by_id_or_raise(
        self, id: IdType, resource_name: str | None = None
    ) -> ModelType:
        """Return a single record by primary key, or raise 404."""
        instance = await self.find_by_id(id)
        if instance is None:
            name = resource_name or self.model.__name__
            raise NotFoundException(name, id)
        return instance

    async def find_by_ids(self, ids: list[IdType]) -> list[ModelType]:
        """Return all records matching the given list of primary keys."""
        if not ids:
            return []
        result = await self.db.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return list(result.scalars().all())

    async def find_one_by(
        self, *conditions: ColumnElement[bool]
    ) -> ModelType | None:
        """Return the first record matching the given conditions.

        Usage::

            user = await repo.find_one_by(User.email == "a@b.com")
        """
        result = await self.db.execute(select(self.model).where(*conditions))
        return result.scalar_one_or_none()

    async def find_many_by(
        self,
        *conditions: ColumnElement[bool],
        skip: int = 0,
        limit: int = 10,
    ) -> list[ModelType]:
        """Return paginated records matching the given conditions.

        Usage::

            active = await repo.find_many_by(
                User.is_active == True, skip=0, limit=20
            )
        """
        result = await self.db.execute(
            select(self.model).where(*conditions).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def find_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        """Return a paginated list of records.

        Parameters
        ----------
        skip:
            Number of rows to skip (offset).
        limit:
            Maximum number of rows to return.
        """
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        """Return the total number of rows for this model."""
        result = await self.db.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def count_by(self, *conditions: ColumnElement[bool]) -> int:
        """Return the number of rows matching the given conditions."""
        result = await self.db.execute(
            select(func.count(self.model.id)).where(*conditions)
        )
        return result.scalar_one()

    # --- Read with relationships (eager loading) ---
    async def find_by_id_with(
        self,
        id: IdType,
        *relationships: QueryableAttribute,
    ) -> ModelType | None:
        """Return a record by primary key with relationships loaded.

        Uses ``selectinload`` to fetch related objects in a
        separate IN query, avoiding N+1 problems.

        Usage::

            user = await repo.find_by_id_with(1, User.roles, User.posts)
        """
        query = select(self.model).where(self.model.id == id)
        for relationship in relationships:
            query = query.options(selectinload(relationship))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_id_with_or_raise(
        self,
        id: IdType,
        *relationships: QueryableAttribute,
        resource_name: str | None = None,
    ) -> ModelType:
        """Return a record by primary key with relationships, or raise 404."""
        instance = await self.find_by_id_with(id, *relationships)
        if instance is None:
            name = resource_name or self.model.__name__
            raise NotFoundException(name, id)
        return instance

    async def find_all_with(
        self,
        *relationships: QueryableAttribute,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ModelType]:
        """Return a paginated list with relationships loaded.

        Usage::

            users = await repo.find_all_with(
                User.roles, User.posts, skip=0, limit=20
            )
        """
        query = select(self.model).offset(skip).limit(limit)
        for relationship in relationships:
            query = query.options(selectinload(relationship))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_many_by_with(
        self,
        *conditions: ColumnElement[bool],
        relationships: list[QueryableAttribute] | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ModelType]:
        """Return filtered records with relationships loaded.

        Usage::

            active_users = await repo.find_many_by_with(
                User.is_active == True,
                relationships=[User.roles],
                skip=0,
                limit=20,
            )
        """
        query = select(self.model).where(*conditions).offset(skip).limit(limit)
        for relationship in relationships or []:
            query = query.options(selectinload(relationship))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_one_by_with(
        self,
        *conditions: ColumnElement[bool],
        relationships: list[QueryableAttribute] | None = None,
    ) -> ModelType | None:
        """Return the first matching record with relationships loaded.

        Usage::

            user = await repo.find_one_by_with(
                User.email == "a@b.com",
                relationships=[User.roles],
            )
        """
        query = select(self.model).where(*conditions)
        for relationship in relationships or []:
            query = query.options(selectinload(relationship))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_with_joined(
        self,
        id: IdType,
        *relationships: QueryableAttribute,
    ) -> ModelType | None:
        """Return a record with relationships loaded via JOIN.

        Uses ``joinedload`` instead of ``selectinload``. Better for
        one-to-one or many-to-one relationships where a single JOIN
        is cheaper than a second query.

        Usage::

            post = await repo.find_with_joined(1, Post.author)
        """
        query = select(self.model).where(self.model.id == id)
        for relationship in relationships:
            query = query.options(joinedload(relationship))
        result = await self.db.execute(query)
        return result.unique().scalar_one_or_none()

    async def refresh_with(
        self,
        instance: ModelType,
        *relationship_names: str,
    ) -> ModelType:
        """Reload an instance with specific relationships populated.

        Useful when you already have an instance but need to access
        a relationship that wasn't eagerly loaded.

        Usage::

            user = await repo.refresh_with(user, "roles", "posts")
            print(user.roles)  # now accessible without lazy load
        """
        await self.db.refresh(instance, list(relationship_names))
        return instance

    # --- Query helpers ---
    async def exists(self, *conditions: ColumnElement[bool]) -> bool:
        """Return ``True`` if at least one record matches the conditions.

        Usage::

            taken = await repo.exists(User.email == "a@b.com")
        """
        result = await self.db.execute(
            select(func.count(self.model.id)).where(*conditions)
        )
        return result.scalar_one() > 0

    # --- Write ---
    async def create(self, **kwargs) -> ModelType:
        """Insert a new row and return the refreshed instance.

        Keyword arguments are forwarded directly to the model
        constructor, so they must match the model's column names.
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def create_from_instance(self, instance: ModelType) -> ModelType:
        """Insert a pre-built model instance and return it refreshed.

        Useful when you need to set relationships or computed fields
        before persisting.
        """
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Apply partial updates to an existing instance.

        Only the supplied keyword arguments are set; other
        attributes remain unchanged.
        """
        for field_name, field_value in kwargs.items():
            setattr(instance, field_name, field_value)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def bulk_update(
        self, *conditions: ColumnElement[bool], **kwargs
    ) -> int:
        """Update all rows matching conditions without loading instances.

        Returns the number of rows affected.

        Usage::

            count = await repo.bulk_update(
                User.is_active == False, is_archived=True
            )
        """
        cursor_result = await self.db.execute(
            update(self.model).where(*conditions).values(**kwargs)
        )
        await self.db.flush()
        return cursor_result.rowcount  # type: ignore[union-attr]

    async def bulk_create(self, items: list[dict]) -> list[ModelType]:
        """Insert multiple rows and return the refreshed instances.

        Parameters
        ----------
        items:
            List of dicts, each forwarded to the model constructor.
        """
        instances = [self.model(**data) for data in items]
        self.db.add_all(instances)
        await self.db.flush()
        ids = [instance.id for instance in instances]
        result = await self.db.execute(
            select(self.model).where(self.model.id.in_(ids))
        )
        return list(result.scalars().all())

    async def delete(self, instance: ModelType) -> None:
        """Mark *instance* for deletion and flush the session."""
        await self.db.delete(instance)
        await self.db.flush()

    async def delete_by_id(self, id: IdType) -> None:
        """Delete a record by primary key, or raise 404 if not found."""
        instance = await self.find_by_id_or_raise(id)
        await self.db.delete(instance)
        await self.db.flush()

    async def bulk_delete(self, *conditions: ColumnElement[bool]) -> int:
        """Delete all rows matching conditions without loading instances.

        Returns the number of rows deleted.

        Usage::

            count = await repo.bulk_delete(User.is_active == False)
        """
        cursor_result = await self.db.execute(
            delete(self.model).where(*conditions)
        )
        await self.db.flush()
        return cursor_result.rowcount  # type: ignore[union-attr]
