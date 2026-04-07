from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.seo_metadata import SeoMetadata
from repositories.base import BaseRepository


class SeoMetadataRepository(BaseRepository[SeoMetadata, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(SeoMetadata, db)
