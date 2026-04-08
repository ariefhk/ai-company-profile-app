from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.company import (
    CompanyAddressRepository,
    CompanyContactRepository,
    CompanyRepository,
    CompanySocialLinkRepository,
)
from schemas.company import (
    CompanyAddressCreate,
    CompanyAddressUpdate,
    CompanyContactCreate,
    CompanyContactUpdate,
    CompanyCreate,
    CompanySocialLinkCreate,
    CompanySocialLinkUpdate,
    CompanyUpdate,
)


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_with_relations(self, id: UUID):
        company = await self.repo.find_with_relations(id)
        if not company:
            await self.repo.find_by_id_or_raise(id)
        return company

    async def get_all(self, skip: int = 0, limit: int = 10):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def create(self, data: CompanyCreate):
        return await self.repo.create(**data.model_dump())

    async def update(self, id: UUID, data: CompanyUpdate):
        company = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(company, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class CompanyContactService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyContactRepository(db)

    async def get_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ):
        return await self.repo.find_by_company(
            company_id, skip=skip, limit=limit
        )

    async def create(self, company_id: UUID, data: CompanyContactCreate):
        return await self.repo.create(
            company_id=company_id, **data.model_dump()
        )

    async def update(self, id: UUID, data: CompanyContactUpdate):
        contact = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(contact, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class CompanySocialLinkService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanySocialLinkRepository(db)

    async def get_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ):
        return await self.repo.find_by_company(
            company_id, skip=skip, limit=limit
        )

    async def create(self, company_id: UUID, data: CompanySocialLinkCreate):
        return await self.repo.create(
            company_id=company_id, **data.model_dump()
        )

    async def update(self, id: UUID, data: CompanySocialLinkUpdate):
        link = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(link, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)


class CompanyAddressService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyAddressRepository(db)

    async def get_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ):
        return await self.repo.find_by_company(
            company_id, skip=skip, limit=limit
        )

    async def create(self, company_id: UUID, data: CompanyAddressCreate):
        return await self.repo.create(
            company_id=company_id, **data.model_dump()
        )

    async def update(self, id: UUID, data: CompanyAddressUpdate):
        address = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(address, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)
