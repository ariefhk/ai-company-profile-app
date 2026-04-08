from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.client import ClientStatus

# --- ClientTestimonial ---


class ClientTestimonialBase(BaseModel):
    author_name: str
    author_role: str | None = None
    content: str
    rating: int | None = None
    is_published: bool = False


class ClientTestimonialCreate(ClientTestimonialBase):
    pass


class ClientTestimonialUpdate(BaseModel):
    author_name: str | None = None
    author_role: str | None = None
    content: str | None = None
    rating: int | None = None
    is_published: bool | None = None


class ClientTestimonialResponse(ClientTestimonialBase):
    id: UUID
    client_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Client ---


class ClientBase(BaseModel):
    name: str
    logo_url: str | None = None
    website_url: str | None = None
    description: str | None = None
    industry: str | None = None
    status: ClientStatus = ClientStatus.active
    sort_order: int = 0


class ClientCreate(ClientBase):
    company_id: UUID


class ClientUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    website_url: str | None = None
    description: str | None = None
    industry: str | None = None
    status: ClientStatus | None = None
    sort_order: int | None = None


class ClientResponse(ClientBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime
    testimonials: list[ClientTestimonialResponse] = []

    model_config = {"from_attributes": True}
