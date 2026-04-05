# Production health check endpoint
from fastapi import APIRouter, Request

from common.response import success_response
from core.config import get_configs

configs = get_configs()
router = APIRouter(tags=["Health"])


@router.get(
    "/health",
)
async def health_check(request: Request):
    return success_response(
        request,
        data={
            "status": "ok",
            "version": configs.APP_VERSION,
            "environment": configs.APP_ENV,
        },
    )
