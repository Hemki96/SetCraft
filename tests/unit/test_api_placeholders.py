from __future__ import annotations

import sys
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

pytest.importorskip("fastapi")
if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)

from app.main import create_app


def test_auth_login_endpoint() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "coach@example.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "placeholder-token"


def test_sources_pipeline_endpoints_create_extract_and_reprocess() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/api/v1/sources",
        json={
            "source_type": "text",
            "content": "4x100 easy\\n8x50 pace",
            "original_filename": "monday.txt",
        },
    )
    assert create_response.status_code == 200
    payload = create_response.json()
    source_id = payload["id"]
    UUID(source_id)
    assert payload["source_status"] == "needs_review"

    list_response = client.get("/api/v1/sources")
    assert list_response.status_code == 200
    assert any(item["id"] == source_id for item in list_response.json()["items"])

    detail_response = client.get(f"/api/v1/sources/{source_id}")
    assert detail_response.status_code == 200
    detail_payload = detail_response.json()
    assert detail_payload["has_raw_text"] is True
    assert detail_payload["extraction_confidence"] >= 0.9

    reprocess_response = client.post(f"/api/v1/sources/{source_id}/reprocess")
    assert reprocess_response.status_code == 200
    assert reprocess_response.json()["source_status"] == "needs_review"


def test_sources_validation_errors_use_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/sources",
        json={"source_type": "unsupported", "content": "x"},
    )

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_source_detail_not_found_uses_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sources/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "Source not found",
        "details": None,
    }
