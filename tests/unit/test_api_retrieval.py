from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_retrieval_search_returns_placeholder_results_without_query() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/retrieval/search")

    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) == 1
    assert payload["items"][0]["id"] == "11111111-1111-1111-1111-111111111111"


def test_retrieval_search_filters_by_query() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/retrieval/search", params={"q": "warmup"})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 1
    assert payload["items"][0]["title"] == "Scaffold Session Placeholder"


def test_retrieval_search_returns_empty_for_non_matching_query() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/retrieval/search", params={"q": "no-match"})

    assert response.status_code == 200
    assert response.json() == {"items": []}
