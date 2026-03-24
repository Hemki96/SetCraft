from __future__ import annotations

import sys
from typing import Any

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)


def _create_source_and_first_session(client: TestClient) -> dict[str, Any]:
    create_source = client.post(
        "/api/v1/sources",
        json={
            "source_type": "text",
            "content": "4x100 easy\\n6x50 kick",
        },
    )
    assert create_source.status_code == 200

    sessions = client.get("/api/v1/sessions")
    assert sessions.status_code == 200
    payload = sessions.json()["items"]
    assert len(payload) >= 1
    return payload[-1]


def test_sessions_list_and_detail_response_shape() -> None:
    client = TestClient(create_app())

    session = _create_source_and_first_session(client)
    session_id = session["id"]

    detail = client.get(f"/api/v1/sessions/{session_id}")
    assert detail.status_code == 200
    assert detail.json()["id"] == session_id
    assert len(detail.json()["blocks"]) >= 1


def test_sessions_review_and_approve_flow() -> None:
    client = TestClient(create_app())

    session = _create_source_and_first_session(client)
    session_id = session["id"]

    approve_before_review = client.post(
        f"/api/v1/sessions/{session_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve_before_review.status_code == 409

    review = client.post(
        f"/api/v1/sessions/{session_id}/review",
        json={"decision": "reviewed", "comment": "Looks good"},
    )
    assert review.status_code == 200
    assert review.json()["review_status"] == "reviewed_ok"
    assert "review_history" in review.json()["details_json"]

    approve = client.post(
        f"/api/v1/sessions/{session_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve.status_code == 200
    assert approve.json()["approval_status"] == "approved"


def test_sessions_patch_endpoints_update_nested_fields() -> None:
    client = TestClient(create_app())

    session = _create_source_and_first_session(client)
    session_id = session["id"]
    block_id = session["blocks"][0]["id"]
    set_id = session["blocks"][0]["sets"][0]["id"]

    patched_session = client.patch(
        f"/api/v1/sessions/{session_id}",
        json={"title": "Updated Session", "tags": ["reviewed"]},
    )
    assert patched_session.status_code == 200
    assert patched_session.json()["title"] == "Updated Session"
    assert patched_session.json()["review_status"] == "pending_review"

    patched_block = client.patch(
        f"/api/v1/sessions/{session_id}/blocks/{block_id}",
        json={"title": "Warmup Block", "block_type": "warmup"},
    )
    assert patched_block.status_code == 200
    assert patched_block.json()["blocks"][0]["title"] == "Warmup Block"

    patched_set = client.patch(
        f"/api/v1/sessions/{session_id}/blocks/{block_id}/sets/{set_id}",
        json={"label": "4x100 aerobic", "distance_m": 400},
    )
    assert patched_set.status_code == 200
    assert patched_set.json()["blocks"][0]["sets"][0]["label"] == "4x100 aerobic"


def test_sessions_explicit_transitions_and_reject_flow() -> None:
    client = TestClient(create_app())
    session = _create_source_and_first_session(client)
    session_id = session["id"]

    start = client.post(f"/api/v1/sessions/{session_id}/review/start")
    assert start.status_code == 200
    assert start.json()["review_status"] == "in_review"

    complete = client.post(
        f"/api/v1/sessions/{session_id}/review/complete",
        json={"review_status": "reviewed_with_changes", "comment": "Adjusted set notes"},
    )
    assert complete.status_code == 200
    assert complete.json()["review_status"] == "reviewed_with_changes"

    submit = client.post(f"/api/v1/sessions/{session_id}/submit-approval")
    assert submit.status_code == 200
    assert submit.json()["approval_status"] == "submitted"

    reject = client.post(
        f"/api/v1/sessions/{session_id}/reject",
        json={"comment": "Please revise"},
        headers={"x-user-role": "admin"},
    )
    assert reject.status_code == 200
    assert reject.json()["approval_status"] == "rejected"

    resubmit = client.post(f"/api/v1/sessions/{session_id}/submit-approval")
    assert resubmit.status_code == 200
    assert resubmit.json()["approval_status"] == "submitted"

    approve = client.post(
        f"/api/v1/sessions/{session_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve.status_code == 200
    assert approve.json()["approval_status"] == "approved"


def test_sessions_invalid_transition_returns_409_with_status_context() -> None:
    client = TestClient(create_app())
    session = _create_source_and_first_session(client)
    session_id = session["id"]

    complete = client.post(
        f"/api/v1/sessions/{session_id}/review/complete",
        json={"review_status": "reviewed_ok"},
    )
    assert complete.status_code == 409
    assert "review_status=" in complete.json()["message"]
    assert "approval_status=" in complete.json()["message"]


def test_session_detail_not_found_uses_standard_error_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/sessions/33333333-3333-3333-3333-333333333333")

    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "Session not found",
        "details": None,
    }
