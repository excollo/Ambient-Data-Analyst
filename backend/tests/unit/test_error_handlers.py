"""Unit tests for global error handlers (sanitized responses, X-Request-ID)."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

from app.core.errors.exceptions import BadRequestError, DatabaseUnavailableError
from app.core.errors.handlers import (
    app_error_handler,
    database_unavailable_handler,
    unhandled_exception_handler,
)


def _mock_request(request_id: str | None = "req-123") -> MagicMock:
    req = MagicMock()
    req.state = MagicMock()
    req.state.request_id = request_id
    return req


def test_app_error_handler_sanitized_and_request_id() -> None:
    req = _mock_request()
    resp = asyncio.run(app_error_handler(req, BadRequestError("bad")))
    assert resp.status_code == 400
    assert resp.body == b'{"detail":"bad"}'
    assert resp.headers.get("x-request-id") == "req-123"


def test_database_unavailable_handler_request_id() -> None:
    req = _mock_request()
    resp = asyncio.run(database_unavailable_handler(req, DatabaseUnavailableError()))
    assert resp.status_code == 503
    assert b"Database unavailable" in resp.body
    assert resp.headers.get("x-request-id") == "req-123"


def test_unhandled_exception_handler_500_no_stack_trace() -> None:
    req = _mock_request()
    resp = asyncio.run(unhandled_exception_handler(req, RuntimeError("secret")))
    assert resp.status_code == 500
    assert resp.body == b'{"detail":"Internal server error"}'
    assert "secret" not in resp.body.decode()
    assert resp.headers.get("x-request-id") == "req-123"
