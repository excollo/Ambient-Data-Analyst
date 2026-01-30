"""Auth API response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class AuthHealthResponse(BaseModel):
    """Auth health check response."""

    status: str = "ok"


class WhoamiResponse(BaseModel):
    """Whoami response: actor and tenant context from request.state."""

    actor: None = None
    tenant_id: str | None
    tenant_slug: str | None


class SignupRequest(BaseModel):
    """Signup request body."""

    email: str
    password: str


class SignupResponse(BaseModel):
    """Signup response (same for new or existing user)."""

    status: str = "ok"
