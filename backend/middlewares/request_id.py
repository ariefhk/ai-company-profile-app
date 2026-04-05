import contextvars
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Context var accessible anywhere during a request lifecycle
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to every request for tracing.

    - Reads X-Request-ID from incoming header (if provided by gateway/LB)
    - Otherwise generates a new UUID
    - Sets it in context var (accessible in logging, services, etc.)
    - Returns it in X-Request-ID response header
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_ctx.set(rid)
        request.state.request_id = rid

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
