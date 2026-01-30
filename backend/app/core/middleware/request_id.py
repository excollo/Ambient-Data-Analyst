"""
Request ID middleware for request tracking.

If the incoming request has an ``X-Request-ID`` header, it is preserved.
Otherwise a new UUID4 is generated. The final ID is attached to the response
as ``X-Request-ID``. Also sets the logging context var for request_id-aware logs.
"""

from __future__ import annotations

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging.setup import request_id_ctx


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a stable X-Request-ID header to every request/response pair."""

    header_name: str = "X-Request-ID"

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        request_id = request.headers.get(self.header_name)
        if not request_id:
            request_id = str(uuid.uuid4())

        request.state.request_id = request_id  # type: ignore[attr-defined]

        token = request_id_ctx.set(request_id)
        try:
            response = await call_next(request)
            response.headers[self.header_name] = request_id
            return response
        finally:
            request_id_ctx.reset(token)


