from __future__ import annotations

import sys

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)

_ADMIN_HEADERS = {"x-user-role": "admin", "x-user-id": "admin-user"}


def _seed_reviewed_session(client: TestClient) -> str:
    created = client.post(
        "/api/v1/sources",
        json={"source_type": "text", "content": "6x100 threshold\\n4x50 kick"},
    )
    assert created.status_code == 200

    sessions = client.get("/api/v1/sessions")
    assert sessions.status_code == 200
    session_id = sessions.json()["items"][0]["id"]

    reviewed = client.post(
        f"/api/v1/sessions/{session_id}/review",
        json={"decision": "reviewed"},
    )
    assert reviewed.status_code == 200
    approved = client.post(f"/api/v1/sessions/{session_id}/approve", headers=_ADMIN_HEADERS)
    assert approved.status_code == 200
    return session_id


def test_generation_set_plan_marks_generated_and_shows_validation_rules() -> None:
    client = TestClient(create_app())
    reference_id = _seed_reviewed_session(client)

    generated = client.post(
        "/api/v1/generation/sets",
        json={"reference_session_ids": [reference_id], "target_distance_m": 1200},
    )
    assert generated.status_code == 200
    payload = generated.json()
    plan_id = payload["id"]
    assert payload["is_generated"] is True
    assert payload["details_json"]["generation_scope"] == "set"

    detail = client.get(f"/api/v1/generation/plans/{plan_id}")
    assert detail.status_code == 200
    rule_codes = [item["rule_code"] for item in detail.json()["validation_results"]]
    assert "manual_review_required" in rule_codes


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

    approve = client.post(f"/api/v1/generation/plans/{plan_id}/approve", headers=_ADMIN_HEADERS)
    assert approve.status_code == 200
    assert approve.json()["approved"] is True
    assert approve.json()["plan"]["approval_status"] == "approved"
    assert len(approve.json()["validation_results"]) >= 1


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

    approve = client.post(f"/api/v1/generation/plans/{plan_id}/approve", headers=_ADMIN_HEADERS)
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
