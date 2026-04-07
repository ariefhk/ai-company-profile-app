from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SeoMetadataBase(BaseModel):
    meta_title: str | None = None
    meta_description: str | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image_url: str | None = None
    canonical_url: str | None = None
    robots: str | None = "index,follow"


class SeoMetadataCreate(SeoMetadataBase):
    pass


class SeoMetadataUpdate(SeoMetadataBase):
    pass


class SeoMetadataResponse(SeoMetadataBase):
    id: UUID
    updated_at: datetime

    model_config = {"from_attributes": True}
