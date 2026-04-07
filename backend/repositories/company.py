from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.company import (
    Company,
    CompanyAddress,
    CompanyContact,
    CompanySocialLink,
)
from repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)

    async def find_with_relations(self, id: UUID) -> Company | None:
        return await self.find_by_id_with(
            id,
            Company.seo,
            Company.contacts,
            Company.social_links,
            Company.addresses,
            Company.clients,
        )


class CompanyContactRepository(BaseRepository[CompanyContact, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompanyContact, db)

    async def find_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[CompanyContact]:
        return await self.find_many_by(
            CompanyContact.company_id == company_id, skip=skip, limit=limit
        )


class CompanySocialLinkRepository(BaseRepository[CompanySocialLink, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompanySocialLink, db)

    async def find_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[CompanySocialLink]:
        return await self.find_many_by(
            CompanySocialLink.company_id == company_id, skip=skip, limit=limit
        )


class CompanyAddressRepository(BaseRepository[CompanyAddress, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(CompanyAddress, db)

    async def find_by_company(
        self, company_id: UUID, skip: int = 0, limit: int = 50
    ) -> list[CompanyAddress]:
        return await self.find_many_by(
            CompanyAddress.company_id == company_id, skip=skip, limit=limit
        )
