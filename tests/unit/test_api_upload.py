from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

pytest.importorskip("fastapi")
if sys.version_info < (3, 12):
    pytest.skip("API tests require Python 3.12+", allow_module_level=True)

from app.core.config import get_settings
from app.main import create_app
from app.services.store import reset_store


@pytest.fixture(autouse=True)
def _reset_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    reset_store()
    monkeypatch.setenv("SOURCE_UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("SOURCE_UPLOAD_MAX_BYTES", "1024")
    get_settings.cache_clear()
    yield
    reset_store()
    get_settings.cache_clear()


def test_upload_accepts_pdf_and_persists_traceable_source() -> None:
    client = TestClient(create_app())
    content = b"%PDF-1.4\n%Test source\n"

    response = client.post(
        "/api/v1/sources/upload",
        params={"source_type": "pdf", "original_filename": "plan.pdf"},
        content=content,
        headers={"content-type": "application/octet-stream"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["source_type"] == "pdf"
    assert payload["source_status"] == "uploaded"
    assert payload["source_reference"].startswith("source://")
    assert payload["storage_key"].endswith(".pdf")
    assert payload["size_bytes"] == len(content)
    assert payload["content_sha256"] == hashlib.sha256(content).hexdigest()

    source_id = payload["id"]
    source_detail_response = client.get(f"/api/v1/sources/{source_id}")
    assert source_detail_response.status_code == 200
    assert source_detail_response.json()["id"] == source_id

    stored_path = Path(get_settings().source_upload_dir) / payload["storage_key"]
    assert stored_path.exists()
    assert stored_path.read_bytes() == content


def test_upload_rejects_content_with_wrong_type_signature() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/sources/upload",
        params={"source_type": "pdf", "original_filename": "plan.pdf"},
        content=b"not-a-pdf",
        headers={"content-type": "application/octet-stream"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "code": "HTTP_ERROR",
        "message": "source_type 'pdf' requires a valid PDF header",
        "details": None,
    }


def test_upload_rejects_oversized_file_without_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOURCE_UPLOAD_MAX_BYTES", "5")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/sources/upload",
        params={"source_type": "text", "original_filename": "plan.txt"},
        content=b"123456",
        headers={"content-type": "application/octet-stream"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "code": "HTTP_ERROR",
        "message": "file exceeds max size (6 > 5 bytes)",
        "details": None,
    }


def test_upload_rejects_path_traversal_in_filename() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/sources/upload",
        params={"source_type": "pdf", "original_filename": "../../etc/passwd"},
        content=b"%PDF-1.4\n",
        headers={"content-type": "application/octet-stream"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "code": "HTTP_ERROR",
        "message": "original_filename contains an invalid path segment",
        "details": None,
    }
