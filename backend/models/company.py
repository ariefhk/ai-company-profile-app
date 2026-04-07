import enum
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.client import Client  # noqa: F401
from models.seo_metadata import SeoMetadata  # noqa: F401


class ContactType(str, enum.Enum):
    phone = "phone"
    email = "email"
    whatsapp = "whatsapp"
    fax = "fax"


class SocialPlatform(str, enum.Enum):
    instagram = "instagram"
    linkedin = "linkedin"
    x = "x"
    youtube = "youtube"
    facebook = "facebook"


class Company(Base):
    __tablename__ = "company"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    seo_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("seo_metadata.id")
    )
    name: Mapped[str] = mapped_column(String(255))
    tagline: Mapped[str | None] = mapped_column(String(255))
    vision: Mapped[str | None] = mapped_column(Text)
    mission: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None] = mapped_column(String(500))
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    founded_year: Mapped[int | None] = mapped_column(Integer)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # relationships
    seo: Mapped["SeoMetadata"] = relationship(back_populates="company")
    contacts: Mapped[list["CompanyContact"]] = relationship(
        back_populates="company"
    )
    social_links: Mapped[list["CompanySocialLink"]] = relationship(
        back_populates="company"
    )
    addresses: Mapped[list["CompanyAddress"]] = relationship(
        back_populates="company"
    )
    clients: Mapped[list["Client"]] = relationship(back_populates="company")


class CompanyContact(Base):
    __tablename__ = "company_contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE")
    )
    type: Mapped[ContactType] = mapped_column(Enum(ContactType))
    label: Mapped[str | None] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(255))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    company: Mapped["Company"] = relationship(back_populates="contacts")


class CompanySocialLink(Base):
    __tablename__ = "company_social_links"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE")
    )
    platform: Mapped[SocialPlatform] = mapped_column(Enum(SocialPlatform))
    url: Mapped[str] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    company: Mapped["Company"] = relationship(back_populates="social_links")


class CompanyAddress(Base):
    __tablename__ = "company_addresses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE")
    )
    label: Mapped[str | None] = mapped_column(String(100))
    street: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(20))
    country: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    company: Mapped["Company"] = relationship(back_populates="addresses")
