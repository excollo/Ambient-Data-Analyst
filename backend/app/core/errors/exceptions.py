"""Custom exception classes."""

from __future__ import annotations


class DatabaseUnavailableError(Exception):
    """
    Raised when the database is unreachable/unhealthy.

    Intentionally does not expose underlying connection errors to callers.
    """

