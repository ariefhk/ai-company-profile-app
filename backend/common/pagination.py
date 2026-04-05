"""
Common pagination utilities for API endpoints.

Provides reusable pagination parameters that can be injected
as FastAPI dependencies to standardize paginated responses.
"""

from fastapi import Query

from core.config import get_configs

configs = get_configs()


class PaginationParams:
    """
    Dependency-injectable pagination parameters for FastAPI endpoints.

    Usage::

        @router.get("/items")
        async def list_items(pagination: PaginationParams = Depends()):
            items = await repo.find(skip=pagination.skip, limit=pagination.limit)

    Attributes:
        page: Current page number (1-indexed).
        limit: Number of items per page, bounded by application config.
        skip: Computed offset for database queries.
    """

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        limit: int = Query(
            default=configs.DEFAULT_PAGE_SIZE,
            ge=1,
            le=configs.MAX_PAGE_SIZE,
            description="Items per page",
        ),
    ):
        self.page = page
        self.limit = limit
        self.skip = (page - 1) * limit
