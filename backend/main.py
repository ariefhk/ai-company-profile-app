from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import router
from common.lifespan import lifespan
from common.rate_limit import limiter
from core.config import get_configs
from middlewares.exception_handler import register_exception_handlers
from middlewares.logging import LoggingMiddleware
from middlewares.request_id import RequestIDMiddleware

configs = get_configs()


def create_app() -> FastAPI:
    app = FastAPI(
        title=configs.APP_NAME,
        version=configs.APP_VERSION,
        docs_url="/docs" if not configs.is_production else None,
        redoc_url="/redoc" if not configs.is_production else None,
        lifespan=lifespan,
    )

    # --- Rate limiter ---
    app.state.limiter = limiter

    # --- Middleware (order matters: last added = first executed) ---
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=configs.CORS_ORIGINS,
        allow_credentials=configs.CORS_ALLOW_CREDENTIALS,
        allow_methods=configs.CORS_ALLOW_METHODS,
        allow_headers=configs.CORS_ALLOW_HEADERS,
    )

    # --- Error handlers ---
    register_exception_handlers(app)

    # --- Routers ---
    app.include_router(router)

    return app


app = create_app()
