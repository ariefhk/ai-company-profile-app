from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from common.security import hash_password, verify_password
from core.exceptions import ConflictException, UnauthorizedException
from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_by_id(self, id: UUID):
        return await self.repo.find_by_id_or_raise(id)

    async def get_all(self, skip: int = 0, limit: int = 10):
        return await self.repo.find_all(skip=skip, limit=limit)

    async def create(self, data: UserCreate):
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise ConflictException(f"Email '{data.email}' is already registered")
        return await self.repo.create(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
        )

    async def update(self, id: UUID, data: UserUpdate):
        user = await self.repo.find_by_id_or_raise(id)
        update_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(user, **update_data)

    async def delete(self, id: UUID):
        await self.repo.delete_by_id(id)

    async def authenticate(self, email: str, password: str):
        user = await self.repo.find_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        return user
