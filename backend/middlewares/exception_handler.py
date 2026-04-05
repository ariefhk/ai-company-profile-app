"""
Global exception handlers for the FastAPI application.

Converts every exception into a consistent JSON error envelope produced
by :func:`common.response.error_response`, so clients always receive a
predictable shape regardless of how the error originated.

Four handler tiers (evaluated in registration order by FastAPI):

1. **AppException** — domain errors raised explicitly in service/router
   code (e.g. ``NotFoundException``, ``ForbiddenException``).
2. **RequestValidationError** — Pydantic / FastAPI request-body and
   query-parameter validation failures (HTTP 422).
3. **StarletteHTTPException** — framework-level HTTP errors such as
   404 route-not-found or 405 method-not-allowed.
4. **Exception (catch-all)** — any unhandled error is logged with a
   full traceback and returned as a generic 500 to avoid leaking
   internal details to the client.

Usage::

    from middleware.exception_handler import register_exception_handlers

    app = FastAPI()
    register_exception_handlers(app)
"""

import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.logging import get_logger
from common.response import error_response
from core.config import get_configs
from core.exceptions import AppException

configs = get_configs()
logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app instance.

    Call this once during application startup, after creating the
    :class:`~fastapi.FastAPI` instance.
    """

    # ── 0. Rate limiting ──────────────────────────────────────────────
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        assert isinstance(exc, RateLimitExceeded)
        return JSONResponse(
            status_code=429,
            content={
                "statusCode": 429,
                "method": request.method,
                "path": str(request.url.path),
                "message": f"Rate limit exceeded: {exc.detail}",
                "error": {"code": "RATE_LIMITED", "details": []},
            },
        )

    # ── 1. Domain exceptions (raised by application code) ────────────
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Map any :class:`~core.exceptions.AppException` subclass to the
        standard error envelope, preserving its status code and details."""
        logger.warning(
            "AppException: %s",
            exc.message,
            extra={
                "extra_data": {
                    "status_code": exc.status_code,
                    "code": exc.code,
                    "path": str(request.url.path),
                    "method": request.method,
                }
            },
        )
        return error_response(
            request,
            status_code=exc.status_code,
            message=exc.message,
            code=exc.code,
            details=exc.details,
        )

    # ── 2. Pydantic / FastAPI validation errors ──────────────────────
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Flatten Pydantic validation errors into a ``details`` list with
        field path, message, and error type for each violated constraint."""
        details = [
            {
                "field": " -> ".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        return error_response(
            request,
            status_code=422,
            message="Validation error",
            code="VALIDATION_ERROR",
            details=details,
        )

    # ── 3. Framework-level HTTP errors ───────────────────────────────
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        """Catch Starlette/FastAPI HTTP exceptions (404, 405, etc.) and
        re-format them into the standard error envelope."""
        return error_response(
            request,
            status_code=exc.status_code,
            message=str(exc.detail),
            code="HTTP_ERROR",
        )

    # ── 4. Catch-all for unexpected errors ───────────────────────────
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Last-resort handler that logs the full traceback and returns a
        generic 500 response to prevent internal details from leaking."""
        logger.error(
            "Unhandled exception: %s",
            str(exc),
            extra={
                "extra_data": {
                    "path": str(request.url.path),
                    "method": request.method,
                    "traceback": traceback.format_exc(),
                }
            },
        )
        message = (
            "Internal server error"
            if configs.is_production
            else f"Internal server error: {exc}"
        )
        return error_response(
            request,
            status_code=500,
            message=message,
            code="INTERNAL_ERROR",
        )
