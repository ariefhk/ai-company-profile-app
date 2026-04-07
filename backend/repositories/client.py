from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.client import Client, ClientStatus, ClientTestimonial
from repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(Client, db)

    async def find_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[Client]:
        return await self.find_many_by(
            Client.company_id == company_id, skip=skip, limit=limit
        )

    async def find_featured(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[Client]:
        return await self.find_many_by(
            Client.company_id == company_id,
            Client.status == ClientStatus.featured,
            skip=skip,
            limit=limit,
        )

    async def find_with_testimonials(self, id: UUID) -> Client | None:
        return await self.find_by_id_with(id, Client.testimonials)


class ClientTestimonialRepository(BaseRepository[ClientTestimonial, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(ClientTestimonial, db)

    async def find_by_client(
        self, client_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[ClientTestimonial]:
        return await self.find_many_by(
            ClientTestimonial.client_id == client_id, skip=skip, limit=limit
        )

    async def find_published(
        self, skip: int = 0, limit: int = 50
    ) -> list[ClientTestimonial]:
        return await self.find_many_by(
            ClientTestimonial.is_published.is_(True), skip=skip, limit=limit
        )
