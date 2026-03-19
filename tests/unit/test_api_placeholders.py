from __future__ import annotations

import sys
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

pytest.importorskip("fastapi")
if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)

from app.main import create_app


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


def test_auth_me_placeholder_endpoint() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "placeholder-user-id",
        "email": "coach@example.com",
        "role": "trainer",
    }


def test_sources_placeholder_endpoints() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/api/v1/sources",
        json={"source_type": "text", "content": "Warmup 400m"},
    )
    assert create_response.status_code == 200
    payload = create_response.json()
    source_id = payload["id"]
    assert payload["source_type"] == "text"
    assert payload["source_status"] == "uploaded"
    UUID(source_id)

    list_response = client.get("/api/v1/sources")
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert len(list_payload["items"]) >= 1
    assert any(item["id"] == source_id for item in list_payload["items"])

    detail_response = client.get(f"/api/v1/sources/{source_id}")
    assert detail_response.status_code == 200
    detail_payload = detail_response.json()
    assert detail_payload["id"] == source_id
    assert detail_payload["source_status"] == "uploaded"

    reprocess_response = client.post(f"/api/v1/sources/{source_id}/reprocess")
    assert reprocess_response.status_code == 200
    reprocess_payload = reprocess_response.json()
    assert reprocess_payload["id"] == source_id
    assert reprocess_payload["source_status"] == "queued"

    queued_response = client.get("/api/v1/sources?source_status=queued")
    assert queued_response.status_code == 200
    queued_items = queued_response.json()["items"]
    assert any(item["id"] == source_id for item in queued_items)

    text_response = client.get("/api/v1/sources?source_type=text")
    assert text_response.status_code == 200
    text_items = text_response.json()["items"]
    assert all(item["source_type"] == "text" for item in text_items)


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


def test_source_detail_not_found_uses_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sources/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "Source not found",
        "details": None,
    }
