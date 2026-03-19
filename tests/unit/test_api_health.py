from __future__ import annotations

import sys

import pytest
from fastapi.testclient import TestClient

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)

from app.main import create_app


def test_health_endpoint_returns_expected_payload() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "setcraft-api",
        "version": "v1",
        "environment": "development",
    }


def test_unknown_route_uses_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/unknown")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "Not Found",
        "details": None,
    }


def test_database_health_endpoint_returns_ok_when_db_is_reachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", lambda: True)
    client = TestClient(create_app())

    response = client.get("/api/v1/health/db")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
    }


def test_database_health_endpoint_returns_503_when_db_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.api.v1.endpoints.health.check_database_connection", lambda: False)
    client = TestClient(create_app())

    response = client.get("/api/v1/health/db")

    assert response.status_code == 503
    assert response.json() == {
        "code": "HTTP_ERROR",
        "message": "Database unavailable",
        "details": None,
    }
