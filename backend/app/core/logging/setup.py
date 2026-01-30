"""
Structured logging setup using Python stdlib only.

Log format includes timestamp, level, logger name, request_id (when available), and message.
Secrets (passwords, tokens, full DATABASE_URL) must never be logged; keep redaction
in application code when logging config or connection info.
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar

# Set by request_id middleware when handling a request.
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """Inject request_id into the log record when available (from context var)."""

    def filter(self, record: logging.LogRecord) -> bool:
        rid = request_id_ctx.get()
        setattr(record, "request_id", rid if rid is not None else "-")
        return True


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure root logging: level, format, and handlers.
    Uses stdlib logging only. Safe to call at startup.
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    fmt = (
        "%(asctime)s | %(levelname)-8s | %(name)s | request_id=%(request_id)s | %(message)s"
    )
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)
