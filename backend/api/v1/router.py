from fastapi import APIRouter

from api.v1.routes import health

router = APIRouter(prefix="/api/v1")

# Register sub-routers
router.include_router(health.router)
