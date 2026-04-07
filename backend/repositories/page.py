from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.page import ContentStatus, Page
from repositories.base import BaseRepository


class PageRepository(BaseRepository[Page, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(Page, db)

    async def find_by_slug(self, slug: str) -> Page | None:
        return await self.find_one_by(Page.slug == slug)

    async def find_published(
        self, skip: int = 0, limit: int = 50
    ) -> list[Page]:
        return await self.find_many_by(
            Page.status == ContentStatus.published, skip=skip, limit=limit
        )

    async def find_with_relations(self, id: UUID) -> Page | None:
        return await self.find_by_id_with(
            id, Page.seo, Page.author, Page.sections
        )

    async def find_by_slug_with_relations(self, slug: str) -> Page | None:
        return await self.find_one_by_with(
            Page.slug == slug,
            relationships=[Page.seo, Page.author, Page.sections],
        )
