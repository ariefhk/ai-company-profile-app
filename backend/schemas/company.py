from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.company import ContactType, SocialPlatform
from schemas.seo_metadata import SeoMetadataResponse

# --- CompanyContact ---


class CompanyContactBase(BaseModel):
    type: ContactType
    label: str | None = None
    value: str
    is_primary: bool = False
    sort_order: int = 0


class CompanyContactCreate(CompanyContactBase):
    pass


class CompanyContactUpdate(BaseModel):
    type: ContactType | None = None
    label: str | None = None
    value: str | None = None
    is_primary: bool | None = None
    sort_order: int | None = None


class CompanyContactResponse(CompanyContactBase):
    id: UUID
    company_id: UUID

    model_config = {"from_attributes": True}


# --- CompanySocialLink ---


class CompanySocialLinkBase(BaseModel):
    platform: SocialPlatform
    url: str
    sort_order: int = 0


class CompanySocialLinkCreate(CompanySocialLinkBase):
    pass


class CompanySocialLinkUpdate(BaseModel):
    platform: SocialPlatform | None = None
    url: str | None = None
    sort_order: int | None = None


class CompanySocialLinkResponse(CompanySocialLinkBase):
    id: UUID
    company_id: UUID

    model_config = {"from_attributes": True}


# --- CompanyAddress ---


class CompanyAddressBase(BaseModel):
    label: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_primary: bool = False


class CompanyAddressCreate(CompanyAddressBase):
    pass


class CompanyAddressUpdate(CompanyAddressBase):
    pass


class CompanyAddressResponse(CompanyAddressBase):
    id: UUID
    company_id: UUID

    model_config = {"from_attributes": True}


# --- Company ---


class CompanyBase(BaseModel):
    name: str
    tagline: str | None = None
    vision: str | None = None
    mission: str | None = None
    description: str | None = None
    logo_url: str | None = None
    cover_image_url: str | None = None
    founded_year: int | None = None


class CompanyCreate(CompanyBase):
    seo_id: UUID | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    tagline: str | None = None
    vision: str | None = None
    mission: str | None = None
    description: str | None = None
    logo_url: str | None = None
    cover_image_url: str | None = None
    founded_year: int | None = None
    seo_id: UUID | None = None


class CompanyResponse(CompanyBase):
    id: UUID
    seo_id: UUID | None = None
    updated_at: datetime
    seo: SeoMetadataResponse | None = None
    contacts: list[CompanyContactResponse] = []
    social_links: list[CompanySocialLinkResponse] = []
    addresses: list[CompanyAddressResponse] = []

    model_config = {"from_attributes": True}
