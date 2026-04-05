"""
HTTP request logging middleware.

Logs every incoming request after the response is produced, capturing
method, path, status code, and round-trip duration in milliseconds.
Each log line includes the ``request_id`` from
:mod:`middleware.request_id` for end-to-end request tracing.

Output is emitted through the structured ``"http"`` logger, so it
respects the format (JSON / text) configured in
:func:`common.logging.setup_logging`.

Example log line (text format)::

    2026-04-03 12:00:00 | INFO     | abc-123 | http:dispatch:25 - GET /tasks -> 200 (12.5ms)
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from common.logging import get_logger
from middlewares.request_id import request_id_ctx

logger = get_logger("http")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log every HTTP request with method, path, status, and duration.

    Sits after :class:`~middleware.request_id.RequestIDMiddleware` in the
    middleware stack so that the correlation ID is available for each log
    entry.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()

        response: Response = await call_next(request)

        # Calculate elapsed time using a monotonic clock to avoid
        # wall-clock drift affecting the measurement.
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        rid = request_id_ctx.get("")

        logger.info(
            "%s %s -> %s (%sms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={"request_id": rid},
        )

        return response
