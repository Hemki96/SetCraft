from __future__ import annotations

import sys
from pathlib import Path

import pytest

API_ROOT = Path(__file__).resolve().parents[2] / "services" / "api"
sys.path.insert(0, str(API_ROOT))

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import create_app  # noqa: E402


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
