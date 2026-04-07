from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.company import Company
    from models.page import Page
    from models.product import Product


class SeoMetadata(Base):
    __tablename__ = "seo_metadata"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    meta_title: Mapped[str | None] = mapped_column(String(160))
    meta_description: Mapped[str | None] = mapped_column(Text)
    og_title: Mapped[str | None] = mapped_column(String(160))
    og_description: Mapped[str | None] = mapped_column(Text)
    og_image_url: Mapped[str | None] = mapped_column(String(500))
    canonical_url: Mapped[str | None] = mapped_column(String(500))
    robots: Mapped[str | None] = mapped_column(
        String(50), default="index,follow"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    company: Mapped[Company] = relationship(back_populates="seo")
    page: Mapped[Page] = relationship(back_populates="seo")
    product: Mapped[Product] = relationship(back_populates="seo")
