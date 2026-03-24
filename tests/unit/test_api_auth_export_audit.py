from __future__ import annotations

import sys

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.audit_service import list_audit_events

if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)


def test_auth_me_uses_default_trainer_role() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "placeholder-user-id",
        "email": "coach@example.com",
        "role": "trainer",
    }


def test_auth_me_honors_role_headers() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/api/v1/auth/me",
        headers={"x-user-id": "admin-1", "x-user-role": "admin"},
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == "admin-1"
    assert response.json()["role"] == "admin"


def test_session_approval_requires_admin_and_is_audited() -> None:
    client = TestClient(create_app())

    review = client.post(
        "/api/v1/sessions/11111111-1111-1111-1111-111111111111/review",
        json={"decision": "reviewed"},
    )
    assert review.status_code == 200

    denied = client.post(
        "/api/v1/sessions/11111111-1111-1111-1111-111111111111/approve",
        headers={"x-user-id": "trainer-1", "x-user-role": "trainer"},
    )
    assert denied.status_code == 403

    events = list_audit_events()
    assert any(
        event.action == "session.approve" and event.outcome == "denied"
        for event in events
    )


def test_export_rejects_non_approved_content_and_audits_attempt() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/exports",
        json={
            "generated_plan_id": "55555555-5555-5555-5555-555555555555",
            "export_format": "json",
        },
        headers={"x-user-id": "trainer-1", "x-user-role": "trainer"},
    )

    assert response.status_code == 409
    assert response.json()["message"] == "Only approved generated plans can be exported"

    events = list_audit_events()
    assert any(
        event.action == "export.create" and event.outcome == "denied"
        for event in events
    )


def test_export_allows_approved_content_and_audits_download() -> None:
    client = TestClient(create_app())

    created = client.post(
        "/api/v1/exports",
        json={
            "generated_plan_id": "44444444-4444-4444-4444-444444444444",
            "export_format": "txt",
        },
        headers={"x-user-id": "trainer-1", "x-user-role": "trainer"},
    )
    assert created.status_code == 200
    export_id = created.json()["id"]

    download = client.get(
        f"/api/v1/exports/{export_id}/download",
        headers={"x-user-id": "trainer-1", "x-user-role": "trainer"},
    )
    assert download.status_code == 200
    assert "Generated Plan:" in download.text

    events = list_audit_events()
    assert any(
        event.action == "export.download" and event.outcome == "success"
        for event in events
    )
