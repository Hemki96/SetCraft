from __future__ import annotations

import hashlib
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from training_plan_schemas.domain_v1 import SourceType

from app.core.config import get_settings

_SOURCE_TYPE_EXTENSION: dict[SourceType, str] = {
    SourceType.PDF: "pdf",
    SourceType.DOCX: "docx",
    SourceType.TEXT: "txt",
}


class UploadValidationError(ValueError):
    pass


@dataclass(frozen=True)
class UploadArtifact:
    storage_key: str
    size_bytes: int
    content_sha256: str


def validate_and_store_upload(
    *,
    source_id: str,
    source_type: SourceType,
    original_filename: str,
    content: bytes,
) -> UploadArtifact:
    _validate_original_filename(original_filename)

    settings = get_settings()
    _validate_max_size(content=content, max_size_bytes=settings.source_upload_max_bytes)
    _validate_content_signature(source_type=source_type, content=content)

    root = Path(settings.source_upload_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    storage_key = f"{source_id}.{_SOURCE_TYPE_EXTENSION[source_type]}"
    storage_path = (root / storage_key).resolve()
    _ensure_within_root(root=root, candidate=storage_path)

    with storage_path.open("xb") as output_file:
        output_file.write(content)

    return UploadArtifact(
        storage_key=storage_key,
        size_bytes=len(content),
        content_sha256=hashlib.sha256(content).hexdigest(),
    )


def _validate_original_filename(filename: str) -> str:
    cleaned = filename.strip()
    if not cleaned:
        raise UploadValidationError("original_filename must not be empty")
    if len(cleaned) > 255:
        raise UploadValidationError("original_filename must not exceed 255 characters")
    if "/" in cleaned or "\\" in cleaned or ".." in cleaned:
        raise UploadValidationError("original_filename contains an invalid path segment")
    if Path(cleaned).name != cleaned:
        raise UploadValidationError("original_filename must be a plain filename")
    return cleaned


def _validate_max_size(*, content: bytes, max_size_bytes: int) -> None:
    if len(content) > max_size_bytes:
        raise UploadValidationError(
            f"file exceeds max size ({len(content)} > {max_size_bytes} bytes)"
        )


def _validate_content_signature(*, source_type: SourceType, content: bytes) -> None:
    if not content:
        raise UploadValidationError("file content must not be empty")

    if source_type is SourceType.PDF:
        if not content.startswith(b"%PDF-"):
            raise UploadValidationError("source_type 'pdf' requires a valid PDF header")
        return

    if source_type is SourceType.DOCX:
        _validate_docx_signature(content)
        return

    if source_type is SourceType.TEXT:
        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise UploadValidationError("source_type 'text' requires UTF-8 content") from exc
        if not decoded.strip():
            raise UploadValidationError("source_type 'text' requires non-empty text content")
        return

    raise UploadValidationError("unsupported source type")


def _validate_docx_signature(content: bytes) -> None:
    if not content.startswith(b"PK"):
        raise UploadValidationError("source_type 'docx' requires a ZIP-based DOCX file")

    try:
        with ZipFile(BytesIO(content)) as archive:
            member_names = set(archive.namelist())
    except BadZipFile as exc:
        raise UploadValidationError("source_type 'docx' requires a valid ZIP container") from exc

    if "[Content_Types].xml" not in member_names:
        raise UploadValidationError("source_type 'docx' missing [Content_Types].xml")
    if not any(name.startswith("word/") for name in member_names):
        raise UploadValidationError("source_type 'docx' missing required /word payload")


def _ensure_within_root(*, root: Path, candidate: Path) -> None:
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise UploadValidationError("resolved storage path escapes upload root") from exc
