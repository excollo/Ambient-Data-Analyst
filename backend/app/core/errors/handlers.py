"""Global error handlers and exception handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.core.errors.exceptions import DatabaseUnavailableError


async def database_unavailable_handler(_: Request, __: DatabaseUnavailableError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DatabaseUnavailableError, database_unavailable_handler)
