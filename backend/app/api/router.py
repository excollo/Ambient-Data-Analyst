"""
Main API router configuration.

This module aggregates versioned and internal API routers into a single
application-wide router.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.internal.routes import router as internal_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.router import v1_router


api_router = APIRouter()

# Internal endpoints (e.g. health checks, diagnostics)
api_router.include_router(internal_router, prefix="/internal", tags=["internal"])

# Public versioned API
api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(v1_router, prefix="/v1", tags=["v1"])


