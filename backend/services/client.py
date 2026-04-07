from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.client import ClientRepository, ClientTestimonialRepository
from schemas.client import (
    ClientCreate,
    ClientTestimonialCreate,
    ClientTestimonialUpdate,
    ClientUpdate,
)


class ClientService:
    def __init__(self, db: AsyncSession):
        self.repo = ClientRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_with_testimonials(self, id: UUID):
        client = await self.repo.find_with_testimonials(id)
        if not client:
            await self.repo.find_by_id_or_raise(id)
        return client

    async def get_by_company(self, company_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_by_company(company_id, skip=skip, limit=limit)

    async def get_featured(self, company_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_featured(company_id, skip=skip, limit=limit)

    async def get_all(self, skip: int = 0, limit: int = 10):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def create(self, data: ClientCreate):
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: ClientUpdate):
        client = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(client, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class ClientTestimonialService:
    def __init__(self, db: AsyncSession):
        self.repo = ClientTestimonialRepository(db)

    async def get_by_client(self, client_id: UUID, skip: int = 0, limit: int = 50):
        return await self.repo.find_by_client(client_id, skip=skip, limit=limit)

    async def get_published(self, skip: int = 0, limit: int = 50):
        return await self.repo.find_published(skip=skip, limit=limit)

    async def create(self, client_id: UUID, data: ClientTestimonialCreate):
        return await self.repo.create(client_id=client_id, **data.model_dump())

    async def update(self, id: UUID, data: ClientTestimonialUpdate):
        testimonial = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(testimonial, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
