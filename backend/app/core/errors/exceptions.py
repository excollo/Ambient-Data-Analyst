"""Custom exception classes."""

from __future__ import annotations


class AppError(Exception):
    """Base for domain exceptions; handlers return sanitized JSON."""

    def __init__(self, message: str = "Application error", status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message=message, status_code=400)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(message=message, status_code=404)


class InternalServerError(AppError):
    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(message=message, status_code=500)


class DatabaseUnavailableError(Exception):
    """
    Raised when the database is unreachable/unhealthy.

    Intentionally does not expose underlying connection errors to callers.
    """

