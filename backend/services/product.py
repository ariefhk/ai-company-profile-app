from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictException
from repositories.product import ProductCategoryRepository, ProductRepository
from schemas.product import (
    ProductCategoryCreate,
    ProductCategoryUpdate,
    ProductCreate,
    ProductUpdate,
)


class ProductCategoryService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductCategoryRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_all(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def get_with_products(self, id: UUID):
        category = await self.repo.find_with_products(id)
        if not category:
            await self.repo.find_by_id_or_raise(id)
        return category

    async def create(self, data: ProductCategoryCreate):
        existing = await self.repo.find_by_slug(data.slug)
        if existing:
            raise ConflictException(f"Category slug '{data.slug}' already exists")
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: ProductCategoryUpdate):
        category = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        if "slug" in update_data:
            existing = await self.repo.find_by_slug(update_data["slug"])
            if existing and existing.id != id:
                raise ConflictException(f"Category slug '{update_data['slug']}' already exists")
        return await self.repo.update(category, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_by_slug(self, slug: str):
        return await self.repo.find_by_slug(slug)

    async def get_with_relations(self, id: UUID):
        product = await self.repo.find_with_relations(id)
        if not product:
            await self.repo.find_by_id_or_raise(id)
        return product

    async def get_all(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def get_published(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_published(skip=skip, limit=limit)

    async def get_by_category(self, category_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_by_category(category_id, skip=skip, limit=limit)

    async def create(self, data: ProductCreate):
        existing = await self.repo.find_by_slug(data.slug)
        if existing:
            raise ConflictException(f"Product slug '{data.slug}' already exists")
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: ProductUpdate):
        product = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        if "slug" in update_data:
            existing = await self.repo.find_by_slug(update_data["slug"])
            if existing and existing.id != id:
                raise ConflictException(f"Product slug '{update_data['slug']}' already exists")
        return await self.repo.update(product, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
