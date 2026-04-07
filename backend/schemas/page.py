from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.page import ContentStatus
from schemas.section import SectionResponse
from schemas.seo_metadata import SeoMetadataResponse
from schemas.user import UserResponse


class PageBase(BaseModel):
    title: str
    slug: str
    body: str | None = None
    status: ContentStatus = ContentStatus.draft


class PageCreate(PageBase):
    seo_id: UUID | None = None
    author_id: UUID | None = None


class PageUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    body: str | None = None
    status: ContentStatus | None = None
    seo_id: UUID | None = None
    author_id: UUID | None = None
    published_at: datetime | None = None


class PageResponse(PageBase):
    id: UUID
    seo_id: UUID | None = None
    author_id: UUID | None = None
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    seo: SeoMetadataResponse | None = None
    author: UserResponse | None = None
    sections: list[SectionResponse] = []

    model_config = {"from_attributes": True}
