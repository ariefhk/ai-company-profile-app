from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from models.section import RefType, SectionType

# --- SectionItem ---


class SectionItemBase(BaseModel):
    ref_type: RefType | None = None
    ref_id: UUID | None = None
    label: str | None = None
    image_url: str | None = None
    url: str | None = None
    sort_order: int = 0


class SectionItemCreate(SectionItemBase):
    pass


class SectionItemUpdate(BaseModel):
    ref_type: RefType | None = None
    ref_id: UUID | None = None
    label: str | None = None
    image_url: str | None = None
    url: str | None = None
    sort_order: int | None = None


class SectionItemResponse(SectionItemBase):
    id: UUID
    section_id: UUID

    model_config = {"from_attributes": True}


# --- Section ---


class SectionBase(BaseModel):
    type: SectionType
    title: str | None = None
    subtitle: str | None = None
    content: str | None = None
    settings: dict[str, Any] | None = None
    sort_order: int = 0
    is_visible: bool = True


class SectionCreate(SectionBase):
    page_id: UUID


class SectionUpdate(BaseModel):
    type: SectionType | None = None
    title: str | None = None
    subtitle: str | None = None
    content: str | None = None
    settings: dict[str, Any] | None = None
    sort_order: int | None = None
    is_visible: bool | None = None


class SectionResponse(SectionBase):
    id: UUID
    page_id: UUID
    created_at: datetime
    updated_at: datetime
    items: list[SectionItemResponse] = []

    model_config = {"from_attributes": True}
