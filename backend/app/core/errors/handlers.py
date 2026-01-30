"""Global error handlers and exception handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.core.errors.exceptions import (
    AppError,
    DatabaseUnavailableError,
)


def _headers_with_request_id(request: Request | None) -> dict[str, str]:
    """Include X-Request-ID in error responses when available (middleware sets it)."""
    if request is None:
        return {}
    rid = getattr(request.state, "request_id", None)
    return {"X-Request-ID": rid} if rid else {}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
        headers=_headers_with_request_id(request),
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers=_headers_with_request_id(request),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers=_headers_with_request_id(request),
    )


async def database_unavailable_handler(
    request: Request, _: DatabaseUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable"},
        headers=_headers_with_request_id(request),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(DatabaseUnavailableError, database_unavailable_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
