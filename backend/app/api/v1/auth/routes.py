"""Auth router: scaffold endpoints for actor/tenant context verification."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.schemas import (
    AuthHealthResponse,
    SignupRequest,
    SignupResponse,
    WhoamiResponse,
)
from app.core.security.auth_service import signup
from app.db.session import get_db

router = APIRouter()


@router.get("/health", response_model=AuthHealthResponse)
async def auth_health() -> AuthHealthResponse:
    """Auth health check."""
    return AuthHealthResponse()


@router.post("/signup", response_model=SignupResponse)
async def signup_endpoint(
    body: SignupRequest,
    db: AsyncSession = Depends(get_db),
) -> SignupResponse:
    """Self-serve signup: creates tenant by domain, adds user. No enumeration."""
    await signup(db, email=body.email, password=body.password)
    await db.commit()
    return SignupResponse()


@router.get("/whoami", response_model=WhoamiResponse)
async def whoami(request: Request) -> WhoamiResponse:
    """Return actor and tenant context from request.state (no secrets, no auth required)."""
    tenant_id = getattr(request.state, "tenant_id", None)
    tenant_slug = getattr(request.state, "tenant_slug", None)
    return WhoamiResponse(actor=None, tenant_id=tenant_id, tenant_slug=tenant_slug)
