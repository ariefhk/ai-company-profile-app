from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.seo_metadata import SeoMetadataRepository
from schemas.seo_metadata import SeoMetadataCreate, SeoMetadataUpdate


class SeoMetadataService:
    def __init__(self, db: AsyncSession):
        self.repo = SeoMetadataRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def create(self, data: SeoMetadataCreate):
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: SeoMetadataUpdate):
        instance = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(instance, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
