from __future__ import annotations

import sys

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)


def _seed_reviewed_session(client: TestClient) -> str:
    created = client.post(
        "/api/v1/sources",
        json={"source_type": "text", "content": "6x100 threshold\\n4x50 kick"},
    )
    assert created.status_code == 200

    sessions = client.get("/api/v1/sessions")
    assert sessions.status_code == 200
    session_id = sessions.json()["items"][-1]["id"]

    reviewed = client.post(
        f"/api/v1/sessions/{session_id}/review",
        json={"decision": "reviewed"},
    )
    assert reviewed.status_code == 200
    approved = client.post(
        f"/api/v1/sessions/{session_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approved.status_code == 200
    return session_id


def test_generation_session_plan_and_approval_flow() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/sessions",
        json={"reference_session_ids": [reference_id], "target_distance_m": 2000},
    )
    assert generated.status_code == 200
    plan_id = generated.json()["id"]
    assert generated.json()["plan_type"] == "session_plan"

    detail = client.get(f"/api/v1/generation/plans/{plan_id}")
    assert detail.status_code == 200
    assert len(detail.json()["validation_results"]) >= 1

    approve = client.post(
        f"/api/v1/generation/plans/{plan_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve.status_code == 200
    assert approve.json()["approved"] is True
    assert approve.json()["plan"]["approval_status"] == "approved"


def test_week_plan_generation_and_export_download() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/week-plans",
        json={
            "reference_session_ids": [reference_id],
            "sessions_per_week": 3,
            "target_total_distance_m": 5400,
        },
    )
    assert generated.status_code == 200
    plan_id = generated.json()["id"]

    approve = client.post(
        f"/api/v1/generation/plans/{plan_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve.status_code == 200
    assert approve.json()["approved"] is True

    export = client.post(
        "/api/v1/exports",
        json={"generated_plan_id": plan_id, "export_format": "json"},
    )
    assert export.status_code == 200
    export_id = export.json()["id"]
    assert export.json()["status"] == "succeeded"

    detail = client.get(f"/api/v1/exports/{export_id}")
    assert detail.status_code == 200
    assert detail.json()["status"] == "succeeded"

    download = client.get(f"/api/v1/exports/{export_id}/download")
    assert download.status_code == 200
    assert download.headers.get("content-disposition")


def test_generated_plan_explicit_review_and_approval_transitions() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/sessions",
        json={"reference_session_ids": [reference_id], "target_distance_m": 2200},
    )
    assert generated.status_code == 200
    plan_id = generated.json()["id"]
    assert generated.json()["review_status"] == "pending_review"
    assert generated.json()["approval_status"] == "not_submitted"

    start = client.post(f"/api/v1/generation/plans/{plan_id}/review/start")
    assert start.status_code == 200
    assert start.json()["review_status"] == "in_review"

    complete = client.post(
        f"/api/v1/generation/plans/{plan_id}/review/complete",
        json={"review_status": "reviewed_ok", "comment": "Looks good"},
    )
    assert complete.status_code == 200
    assert complete.json()["review_status"] == "reviewed_ok"

    submit = client.post(f"/api/v1/generation/plans/{plan_id}/submit-approval")
    assert submit.status_code == 200
    assert submit.json()["approval_status"] == "submitted"

    approve = client.post(
        f"/api/v1/generation/plans/{plan_id}/approve",
        headers={"x-user-role": "admin"},
    )
    assert approve.status_code == 200
    assert approve.json()["plan"]["approval_status"] == "approved"


def test_generated_plan_transition_conflict_returns_409_with_status_context() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/week-plans",
        json={
            "reference_session_ids": [reference_id],
            "sessions_per_week": 2,
            "target_total_distance_m": 3600,
        },
    )
    assert generated.status_code == 200
    plan_id = generated.json()["id"]

    complete = client.post(
        f"/api/v1/generation/plans/{plan_id}/review/complete",
        json={"review_status": "reviewed_with_changes"},
    )
    assert complete.status_code == 409
    assert "review_status=" in complete.json()["message"]
    assert "approval_status=" in complete.json()["message"]


def test_generated_plan_reject_transition_requires_submitted_state() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/sessions",
        json={"reference_session_ids": [reference_id], "target_distance_m": 1800},
    )
    assert generated.status_code == 200
    plan_id = generated.json()["id"]

    reject_before_submit = client.post(
        f"/api/v1/generation/plans/{plan_id}/reject",
        json={"comment": "Not ready"},
        headers={"x-user-role": "admin"},
    )
    assert reject_before_submit.status_code == 409

    client.post(f"/api/v1/generation/plans/{plan_id}/review/start")
    client.post(
        f"/api/v1/generation/plans/{plan_id}/review/complete",
        json={"review_status": "reviewed_ok"},
    )
    client.post(f"/api/v1/generation/plans/{plan_id}/submit-approval")

    reject_after_submit = client.post(
        f"/api/v1/generation/plans/{plan_id}/reject",
        json={"comment": "Revise pacing"},
        headers={"x-user-role": "admin"},
    )
    assert reject_after_submit.status_code == 200
    assert reject_after_submit.json()["approval_status"] == "rejected"
