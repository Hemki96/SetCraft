from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_sessions_list_placeholder_response_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sessions")

    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) == 1

    session = payload["items"][0]
    assert session["id"] == "11111111-1111-1111-1111-111111111111"
    assert session["source_file_id"] == "22222222-2222-2222-2222-222222222222"
    assert session["review_status"] == "needs_review"
    assert session["approval_status"] == "pending"
    assert isinstance(session["blocks"], list)
    assert len(session["blocks"]) == 1


def test_session_detail_placeholder_found() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sessions/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "11111111-1111-1111-1111-111111111111"
    assert payload["title"] == "Scaffold Session Placeholder"


def test_session_detail_placeholder_not_found_uses_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sessions/33333333-3333-3333-3333-333333333333")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "Session not found",
        "details": None,
    }
