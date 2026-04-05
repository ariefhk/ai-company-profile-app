"""Seed initial users into the database."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.security import hash_password
from models.user import User, UserRole

USERS = [
    {
        "name": "Admin",
        "email": "admin@example.com",
        "password_hash": hash_password("admin123"),
        "role": UserRole.ADMIN,
    },
    {
        "name": "User",
        "email": "user@example.com",
        "password_hash": hash_password("user123"),
        "role": UserRole.USER,
    },
]


async def run(db: AsyncSession) -> None:
    for user_data in USERS:
        result = await db.execute(
            select(User).where(User.email == user_data["email"])
        )
        existing = result.scalar_one_or_none()

        if existing is None:
            db.add(User(**user_data))
