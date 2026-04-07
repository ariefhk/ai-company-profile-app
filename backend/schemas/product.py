from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from models.page import ContentStatus
from schemas.seo_metadata import SeoMetadataResponse

# --- ProductCategory ---


class ProductCategoryBase(BaseModel):
    name: str
    slug: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class ProductCategoryResponse(ProductCategoryBase):
    id: UUID

    model_config = {"from_attributes": True}


# --- Product ---


class ProductBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    thumbnail_url: str | None = None
    price_original: Decimal | None = None
    price_underline: Decimal | None = None
    status: ContentStatus = ContentStatus.draft


class ProductCreate(ProductBase):
    seo_id: UUID | None = None
    category_id: UUID | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    price_original: Decimal | None = None
    price_underline: Decimal | None = None
    status: ContentStatus | None = None
    seo_id: UUID | None = None
    category_id: UUID | None = None


class ProductResponse(ProductBase):
    id: UUID
    seo_id: UUID | None = None
    category_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    seo: SeoMetadataResponse | None = None
    category: ProductCategoryResponse | None = None

    model_config = {"from_attributes": True}
