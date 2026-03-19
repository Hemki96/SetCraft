from __future__ import annotations

import pytest

pytest.importorskip("fastapi")

from app.main import create_app
from fastapi.testclient import TestClient


def test_auth_login_placeholder_endpoint() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "coach@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "placeholder-token",
        "token_type": "bearer",
        "expires_in": 3600,
    }


def test_sources_placeholder_endpoints() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/api/v1/sources",
        json={"source_type": "text", "content": "Warmup 400m"},
    )
    assert create_response.status_code == 200
    payload = create_response.json()
    assert payload["source_type"] == "text"
    assert payload["source_status"] == "uploaded"

    list_response = client.get("/api/v1/sources")
    assert list_response.status_code == 200
    assert list_response.json() == {"items": []}


def test_sources_validation_errors_use_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/sources",
        json={"source_type": "unsupported", "content": "x"},
    )

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
    assert response.json()["message"] == "Request validation failed"
    assert "errors" in (response.json().get("details") or {})
