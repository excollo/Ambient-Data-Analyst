"""V1 API router: aggregates public endpoints (auth is mounted separately with auth tag only)."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routes import router as v1_routes

v1_router = APIRouter()
v1_router.include_router(v1_routes)
