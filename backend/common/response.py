import math
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


def success_response(
    request: Request,
    data: Any,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    """Build a standardized JSON success response.

    Args:
        request: The incoming FastAPI request, used to extract method and path.
        data: The response payload to include under the "data" key.
        message: A human-readable status message. Defaults to "Success".
        status_code: HTTP status code for the response. Defaults to 200.

    Returns:
        A JSONResponse with a consistent envelope containing statusCode,
        method, path, message, and data.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "method": request.method,
            "path": str(request.url.path),
            "message": message,
            "data": data,
        },
    )


def success_list_response(
    request: Request,
    data: list[Any],
    total_items: int,
    page: int,
    limit: int,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    """Build a standardized JSON success response for paginated lists.

    Args:
        request: The incoming FastAPI request, used to extract method and path.
        data: The list of items for the current page.
        total_items: Total number of items across all pages.
        page: The current page number (1-indexed).
        limit: Maximum number of items per page.
        message: A human-readable status message. Defaults to "Success".
        status_code: HTTP status code for the response. Defaults to 200.

    Returns:
        A JSONResponse with a consistent envelope containing statusCode,
        method, path, message, data, and pagination meta (page, limit,
        total_items, total_pages, has_next_page, has_prev_page).
    """
    # Calculate total pages
    if limit > 0:
        total_pages = math.ceil(total_items / limit)
    else:
        total_pages = 0

    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "method": request.method,
            "path": str(request.url.path),
            "message": message,
            "data": data,
            "meta": {
                "page": page,
                "limit": limit,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next_page": page < total_pages,
                "has_prev_page": page > 1,
            },
        },
    )


def error_response(
    request: Request,
    status_code: int,
    message: str,
    code: str = "ERROR",
    details: list | None = None,
) -> JSONResponse:
    """Build a standardized JSON error response.

    Args:
        request: The incoming FastAPI request, used to extract method and path.
        status_code: HTTP status code for the error response.
        message: A human-readable error description.
        code: A machine-readable error code. Defaults to "ERROR".
        details: Optional list of granular error details (e.g. validation errors).

    Returns:
        A JSONResponse with a consistent envelope containing statusCode,
        method, path, message, and an error object with code and details.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "method": request.method,
            "path": str(request.url.path),
            "message": message,
            "error": {
                "code": code,
                "details": details if details is not None else [],
            },
        },
    )
