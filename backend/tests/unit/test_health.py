from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_internal_healthz() -> None:
    response = client.get("/internal/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_v1_health() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_tenant_required_returns_400_without_header() -> None:
    """Tenant middleware blocks /internal/tenant when X-Tenant-ID is missing."""
    response = client.get("/internal/tenant")
    assert response.status_code == 400
    assert response.json()["detail"] == "X-Tenant-ID header required"


