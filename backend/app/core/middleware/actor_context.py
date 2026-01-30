"""
Actor context stub for future auth integration.

Sets request.state.actor = None. No token parsing or auth logic.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class ActorContextMiddleware(BaseHTTPMiddleware):
    """Set request.state.actor = None as a stub for future auth."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        request.state.actor = None  # type: ignore[attr-defined]
        return await call_next(request)
