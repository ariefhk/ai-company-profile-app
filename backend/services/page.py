from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ConflictException
from repositories.page import PageRepository
from schemas.page import PageCreate, PageUpdate


class PageService:
    def __init__(self, db: AsyncSession):
        self.repo = PageRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_by_slug(self, slug: str):
        return await self.repo.find_by_slug(slug)

    async def get_with_relations(self, id: UUID):
        page = await self.repo.find_with_relations(id)
        if not page:
            await self.repo.find_by_id_or_raise(id)
        return page

    async def get_by_slug_with_relations(self, slug: str):
        return await self.repo.find_by_slug_with_relations(slug)

    async def get_all(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def get_published(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_published(skip=skip, limit=limit)

    async def create(self, data: PageCreate):
        existing = await self.repo.find_by_slug(data.slug)
        if existing:
            raise ConflictException(f"Page slug '{data.slug}' already exists")
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: PageUpdate):
        page = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        if "slug" in update_data:
            existing = await self.repo.find_by_slug(update_data["slug"])
            if existing and existing.id != id:
                raise ConflictException(f"Page slug '{update_data['slug']}' already exists")
        return await self.repo.update(page, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
