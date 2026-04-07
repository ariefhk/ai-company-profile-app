from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def find_by_email(self, email: str) -> User | None:
        return await self.find_one_by(User.email == email)
