"""
Tenant header enforcement middleware.

Enforces X-Tenant-ID for tenant-required routes. Skips enforcement for auth
endpoints (signup, health, whoami, and future login/verify/resend).
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

# Paths where X-Tenant-ID is NOT required (auth endpoints)
# TODO: add /v1/auth/login, /v1/auth/verify, /v1/auth/resend when implemented
TENANT_SKIP_PATHS = frozenset(["/v1/auth/signup", "/v1/auth/health", "/v1/auth/whoami"])

# Paths that require X-Tenant-ID
TENANT_REQUIRED_PATHS = frozenset(["/internal/tenant"])


class TenantEnforcementMiddleware(BaseHTTPMiddleware):
    """Enforce X-Tenant-ID header for tenant-required routes only."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        path = request.scope.get("path", "")

        if path in TENANT_SKIP_PATHS:
            return await call_next(request)

        if path in TENANT_REQUIRED_PATHS:
            if not request.headers.get("X-Tenant-ID"):
                rid = getattr(request.state, "request_id", None)
                headers = {"X-Request-ID": rid} if rid else {}
                return JSONResponse(
                    status_code=400,
                    content={"detail": "X-Tenant-ID header required"},
                    headers=headers,
                )

        return await call_next(request)
