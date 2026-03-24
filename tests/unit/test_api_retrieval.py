from __future__ import annotations

import sys

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)


def _seed_session(client: TestClient) -> None:
    response = client.post(
        "/api/v1/sources",
        json={
            "source_type": "text",
            "content": "4x100 warmup\\n8x50 sprint",
        },
    )
    assert response.status_code == 200


def test_retrieval_search_returns_seeded_results_without_query() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 1
    assert payload["semantic_enabled"] is True
    assert len(payload["matches"]) == 1
    assert payload["matches"][0]["combined_score"] == 0.0


def test_retrieval_search_filters_by_query_with_hybrid_scores() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search", params={"q": "warmup"})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 1
    assert payload["matches"][0]["combined_score"] > 0.0


def test_retrieval_search_returns_empty_for_non_matching_query() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get("/api/v1/retrieval/search", params={"q": "no-match"})

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["matches"] == []


def test_retrieval_search_applies_structured_filters() -> None:
    client = TestClient(create_app())
    _seed_session(client)

    response = client.get(
        "/api/v1/retrieval/search",
        params={"distance_m": 800},
    )

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

    response_outside = client.get(
        "/api/v1/retrieval/search",
        params={"distance_m": 5000},
    )
    assert response_outside.status_code == 200
    assert response_outside.json()["items"] == []
