"""
Application-level exception hierarchy.

All domain exceptions inherit from :class:`AppException`, which carries
an HTTP status code, a human-readable message, a machine-readable code,
and optional structured details.  These are caught by the global
exception handler registered in ``middleware.exception_handler`` and
serialized into the standard error-response envelope defined in
``common.response.error_response``.

Usage::

    from core.exceptions import NotFoundException

    raise NotFoundException("Task", task_id)

Response::

    {
        "statusCode": 404,
        "message": "Task with id '42' not found",
        "error": {"code": "NOT_FOUND", "details": []}
    }
"""


from uuid import UUID


class AppException(Exception):
    """Base exception for all application-level errors.

    Attributes:
        status_code: HTTP status code returned to the client.
        message: Human-readable error description.
        code: Machine-readable error identifier (e.g. ``"NOT_FOUND"``).
        details: Optional list of granular sub-errors (e.g. field-level validation failures).
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        code: str,
        details: list | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.code = code
        if details is not None:
            self.details = details
        else:
            self.details = []


class NotFoundException(AppException):
    """Raised when a requested resource does not exist (HTTP 404)."""

    def __init__(self, resource: str, resource_id: int | str | UUID):
        super().__init__(
            404, f"{resource} with id '{resource_id}' not found", "NOT_FOUND"
        )


class BadRequestException(AppException):
    """Raised when the client sends an invalid or malformed request (HTTP 400)."""

    def __init__(self, message: str, details: list | None = None):
        super().__init__(400, message, "BAD_REQUEST", details)


class UnauthorizedException(AppException):
    """Raised when authentication is missing or invalid (HTTP 401)."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(401, message, "UNAUTHORIZED")


class ForbiddenException(AppException):
    """Raised when the user lacks permission for the action (HTTP 403)."""

    def __init__(
        self, message: str = "You don't have permission to perform this action"
    ):
        super().__init__(403, message, "FORBIDDEN")


class ConflictException(AppException):
    """Raised when the request conflicts with current resource state (HTTP 409)."""

    def __init__(self, message: str):
        super().__init__(409, message, "CONFLICT")
