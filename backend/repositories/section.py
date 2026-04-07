from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.section import Section, SectionItem
from repositories.base import BaseRepository


class SectionRepository(BaseRepository[Section, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(Section, db)

    async def find_by_page(
        self, page_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[Section]:
        return await self.find_many_by(
            Section.page_id == page_id, skip=skip, limit=limit
        )

    async def find_with_items(self, id: UUID) -> Section | None:
        return await self.find_by_id_with(id, Section.items)

    async def find_visible_by_page(
        self, page_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[Section]:
        return await self.find_many_by(
            Section.page_id == page_id,
            Section.is_visible.is_(True),
            skip=skip,
            limit=limit,
        )


class SectionItemRepository(BaseRepository[SectionItem, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(SectionItem, db)

    async def find_by_section(
        self, section_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[SectionItem]:
        return await self.find_many_by(
            SectionItem.section_id == section_id, skip=skip, limit=limit
        )
