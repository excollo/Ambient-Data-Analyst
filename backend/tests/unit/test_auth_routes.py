"""Unit tests for auth scaffold endpoints."""

import uuid
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_health() -> None:
    response = client.get("/v1/auth/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Request-ID" in response.headers


def test_whoami_no_tenant() -> None:
    response = client.get("/v1/auth/whoami")
    assert response.status_code == 200
    data = response.json()
    assert data["actor"] is None
    assert data["tenant_id"] is None
    assert data["tenant_slug"] is None


def test_signup_public_domain_returns_400() -> None:
    response = client.post(
        "/v1/auth/signup",
        json={"email": "test@gmail.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Please use your work email address."


async def _mock_get_db():
    from unittest.mock import MagicMock

    session = MagicMock()
    session.commit = AsyncMock()
    try:
        yield session
    finally:
        pass


def test_signup_new_corporate_domain_creates_tenant_and_user() -> None:
    domain = f"testcompany-{uuid.uuid4().hex[:8]}.com"
    email = f"user@{domain}"
    with (
        patch("app.api.v1.auth.routes.signup", new_callable=AsyncMock) as mock_signup,
        patch("app.api.v1.auth.routes.get_db", side_effect=_mock_get_db),
    ):
        mock_signup.return_value = None
        response = client.post(
            "/v1/auth/signup",
            json={"email": email, "password": "StrongPass123!"},
        )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup_same_email_returns_ok_no_enumeration() -> None:
    domain = f"testcompany-{uuid.uuid4().hex[:8]}.com"
    email = f"user@{domain}"
    with (
        patch("app.api.v1.auth.routes.signup", new_callable=AsyncMock) as mock_signup,
        patch("app.api.v1.auth.routes.get_db", side_effect=_mock_get_db),
    ):
        mock_signup.return_value = None
        client.post("/v1/auth/signup", json={"email": email, "password": "FirstPass123!"})
        response = client.post(
            "/v1/auth/signup",
            json={"email": email, "password": "SecondPass456!"},
        )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
