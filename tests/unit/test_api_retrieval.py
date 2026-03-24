from __future__ import annotations

import sys

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)


def _seed_session(client: TestClient) -> tuple[str, str, str]:
    response = client.post(
        "/api/v1/sources",
        json={
            "source_type": "text",
            "content": "4x100 warmup\\n8x50 sprint",
        },
    )
    assert response.status_code == 200

    sessions = client.get("/api/v1/sessions")
    assert sessions.status_code == 200
    session = sessions.json()["items"][-1]
    block_id = session["blocks"][0]["id"]
    set_id = session["blocks"][0]["sets"][0]["id"]

    patch_block = client.patch(
        f"/api/v1/sessions/{session['id']}/blocks/{block_id}",
        json={"block_type": "warmup"},
    )
    assert patch_block.status_code == 200

    patch_set = client.patch(
        f"/api/v1/sessions/{session['id']}/blocks/{block_id}/sets/{set_id}",
        json={"intensity_note": "high", "tags": ["sprint"]},
    )
    assert patch_set.status_code == 200

    return session["id"], block_id, set_id


def test_retrieval_search_returns_seeded_results_without_query() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) >= 1
    assert payload["semantic_enabled"] is True


def test_retrieval_search_filters_by_query() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search", params={"q": "warmup"})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) >= 1


def test_retrieval_search_returns_empty_for_non_matching_query() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search", params={"q": "no-match"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"] == []
    assert payload["matches"] == []


def test_retrieval_search_applies_structured_filters() -> None:
    client = TestClient(create_app())
    session_id, _, _ = _seed_session(client)

    response = client.get(
        "/api/v1/retrieval/search",
        params={"min_distance_m": 700, "max_distance_m": 1200},
    )

    assert response.status_code == 200
    ids = {item["id"] for item in response.json()["items"]}
    assert session_id in ids

    response_outside = client.get(
        "/api/v1/retrieval/search",
        params={"min_distance_m": 5000},
    )
    assert response_outside.status_code == 200
    assert response_outside.json()["items"] == []


def test_retrieval_search_filters_by_intensity_and_type() -> None:
    client = TestClient(create_app())
    session_id, _, _ = _seed_session(client)

    by_intensity = client.get(
        "/api/v1/retrieval/search",
        params={"intensity": "high"},
    )
    assert by_intensity.status_code == 200
    intensity_ids = {item["id"] for item in by_intensity.json()["items"]}
    assert session_id in intensity_ids

    by_type = client.get(
        "/api/v1/retrieval/search",
        params={"type": "warmup"},
    )
    assert by_type.status_code == 200
    type_ids = {item["id"] for item in by_type.json()["items"]}
    assert session_id in type_ids


def test_retrieval_search_review_status_filter_supports_legacy_value() -> None:
    client = TestClient(create_app())
    session_id, _, _ = _seed_session(client)

    review = client.post(
        f"/api/v1/sessions/{session_id}/review",
        json={"decision": "reviewed"},
    )
    assert review.status_code == 200

    by_legacy_review = client.get(
        "/api/v1/retrieval/search",
        params={"review_status": "reviewed"},
    )
    assert by_legacy_review.status_code == 200
    ids = {item["id"] for item in by_legacy_review.json()["items"]}
    assert session_id in ids
