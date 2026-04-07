from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.section import SectionItemRepository, SectionRepository
from schemas.section import (
    SectionCreate,
    SectionItemCreate,
    SectionItemUpdate,
    SectionUpdate,
)


class SectionService:
    def __init__(self, db: AsyncSession):
        self.repo = SectionRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_with_items(self, id: UUID):
        section = await self.repo.find_with_items(id)
        if not section:
            await self.repo.find_by_id_or_raise(id)
        return section

    async def get_by_page(self, page_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_by_page(page_id, skip=skip, limit=limit)

    async def get_visible_by_page(self, page_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_visible_by_page(page_id, skip=skip, limit=limit)

    async def create(self, data: SectionCreate):
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: SectionUpdate):
        section = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(section, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class SectionItemService:
    def __init__(self, db: AsyncSession):
        self.repo = SectionItemRepository(db)

    async def get_by_section(self, section_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_by_section(section_id, skip=skip, limit=limit)

    async def create(self, section_id: UUID, data: SectionItemCreate):
        return await self.repo.create(section_id=section_id, **data.model_dump())

    async def update(self, id: UUID, data: SectionItemUpdate):
        item = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(item, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
