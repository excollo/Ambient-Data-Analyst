"""
FastAPI application entry point.

This module creates the FastAPI app, installs middleware, and includes
the main API router.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router
from app.core.middleware.request_id import RequestIDMiddleware
from app.core.config.settings import settings
import logging

logger = logging.getLogger("ambient.env")

def _redact_db_url(url: str) -> str:
    # redact credentials but keep host/DB visible
    if "://" not in url or "@" not in url:
        return url
    scheme, rest = url.split("://", 1)
    creds, host = rest.split("@", 1)
    return f"{scheme}://***@{host}"

def create_app() -> FastAPI:
    """Application factory used for both runtime and testing."""
    app = FastAPI()

    # Middleware
    app.add_middleware(RequestIDMiddleware)

    # API routers
    app.include_router(api_router)

    logger.info(
        "Booting Ambient backend ENVIRONMENT=%s DATABASE_URL=%s",
        settings.ENVIRONMENT,
        _redact_db_url(settings.DATABASE_URL),
    )

    return app


app = create_app()


