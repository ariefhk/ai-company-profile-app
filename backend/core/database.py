"""
Async SQLAlchemy database engine and session configuration.

Creates a single :class:`~sqlalchemy.ext.asyncio.AsyncEngine` from the
``DATABASE_URL`` defined in application config and exposes an
:class:`~sqlalchemy.ext.asyncio.AsyncSession` factory for
request-scoped sessions.

Usage::

    from core.database import get_db
    from models.base import Base

    # Dependency injection (FastAPI)
    async def my_route(db: AsyncSession = Depends(get_db)):
        ...
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import get_configs

configs = get_configs()

# SQLite requires aiosqlite driver for async.
connect_args = {}
if configs.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

_pool_kwargs: dict = {"pool_pre_ping": True}

if not configs.DATABASE_URL.startswith("sqlite"):
    _pool_kwargs["pool_size"] = configs.DB_POOL_SIZE
    _pool_kwargs["max_overflow"] = configs.DB_MAX_OVERFLOW
    _pool_kwargs["pool_recycle"] = configs.DB_POOL_RECYCLE
    _pool_kwargs["pool_timeout"] = configs.DB_POOL_TIMEOUT

engine = create_async_engine(
    configs.DATABASE_URL,
    connect_args=connect_args,
    **_pool_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Provide a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
