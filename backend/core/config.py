from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    # App
    APP_NAME: str = "Arief FastApi Template"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"  # development, staging, production
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_company_profile"

    # Auth
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = [
        "GET",
        "POST",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ]
    CORS_ALLOW_HEADERS: list[str] = ["Authorization", "Content-Type"]

    # Database Pool (ignored for SQLite)
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_TIMEOUT: int = 30

    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "60/minute"
    RATE_LIMIT_AUTH: str = "5/minute"

    # Scheduler
    SCHEDULER_ENABLED: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.APP_ENV == "production":
            if (
                self.SECRET_KEY == "change-me-in-production"
                or len(self.SECRET_KEY) < 32
            ):
                raise ValueError(
                    "SECRET_KEY must be changed and at least 32 characters in production"
                )
            if self.DATABASE_URL.startswith("sqlite"):
                raise ValueError(
                    "SQLite is not supported in production. Use PostgreSQL."
                )
            if self.DEBUG:
                raise ValueError("DEBUG must be False in production")
        return self

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache
def get_configs() -> Configs:
    return Configs()
