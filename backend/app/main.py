"""
FastAPI application entry point.

This module creates the FastAPI app, installs middleware, and includes
the main API router.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.router import api_router
from app.core.config.settings import settings
from app.core.errors.handlers import register_exception_handlers
from app.core.logging.setup import configure_logging
from app.core.middleware.actor_context import ActorContextMiddleware
from app.core.middleware.request_id import RequestIDMiddleware
from app.core.middleware.tenant_enforcement import TenantEnforcementMiddleware

logger = logging.getLogger(__name__)


def _redact_db_url(url: str) -> str:
    """Redact credentials but keep host/db visible; never log full DATABASE_URL."""
    if "://" not in url or "@" not in url:
        return url
    scheme, rest = url.split("://", 1)
    creds, host = rest.split("@", 1)
    return f"{scheme}://***@{host}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init logging, then boot log. Shutdown: none for now."""
    configure_logging(settings.LOG_LEVEL)
    logger.info(
        "Booting Ambient backend ENVIRONMENT=%s DATABASE_URL=%s",
        settings.ENVIRONMENT,
        _redact_db_url(settings.DATABASE_URL),
    )
    yield


def create_app() -> FastAPI:
    """Application factory used for both runtime and testing."""
    app = FastAPI(
        title="Ambient Data Analyst API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.DOCS_ENABLED else None,
        redoc_url="/redoc" if settings.DOCS_ENABLED else None,
    )

    register_exception_handlers(app)
    app.add_middleware(TenantEnforcementMiddleware)
    app.add_middleware(ActorContextMiddleware)  # stub: request.state.actor = None
    app.add_middleware(RequestIDMiddleware)
    app.include_router(api_router)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            routes=app.routes,
        )
        openapi_schema.setdefault("components", {})
        openapi_schema["components"].setdefault("securitySchemes", {})
        openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app


app = create_app()


