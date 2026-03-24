from __future__ import annotations

from uuid import UUID

from training_plan_schemas.domain_v1 import SourceFile, SourceStatus, SourceType

from app.schemas.sources import (
    SourceCreateRequest,
    SourceDetail,
    SourceListResponse,
    SourceSummary,
    SourceUploadResponse,
)
from app.services.extraction_service import extract_text
from app.services.normalization_service import normalize_to_session
from app.services.store import STORE, SourceRecord
from app.services.upload_service import validate_and_store_upload

# Backward-compatible alias for existing imports in tests/tools.
SOURCE_STORE = STORE.sources


def _to_summary(source: SourceFile) -> SourceSummary:
    return SourceSummary(
        id=source.id,
        source_type=source.source_type,
        source_status=source.source_status,
        original_filename=source.original_filename,
        ingested_at=source.ingested_at,
    )


def _run_ingestion_pipeline(source_id: UUID) -> None:
    record = STORE.sources[source_id]
    source = record.source

    source.source_status = SourceStatus.EXTRACTING
    extracted = extract_text(source_type=source.source_type, content=record.content)

    source.raw_text = extracted.raw_text
    source.source_status = SourceStatus.EXTRACTED
    record.extraction_confidence = extracted.confidence

    source.source_status = SourceStatus.NORMALIZING
    session = normalize_to_session(source_file_id=source.id, segments=extracted.segments)
    STORE.sessions[session.id] = session
    record.session_ids = [session.id]

    source.source_status = SourceStatus.NEEDS_REVIEW


def create_source(payload: SourceCreateRequest) -> SourceSummary:
    with STORE.lock:
        source = SourceFile(
            source_type=payload.source_type,
            original_filename=payload.original_filename,
            source_status=SourceStatus.UPLOADED,
        )
        record = SourceRecord(source=source, content=payload.content)
        STORE.sources[source.id] = record

        source.source_status = SourceStatus.QUEUED
        _run_ingestion_pipeline(source.id)
        return _to_summary(source)


def list_sources(
    *,
    source_status: SourceStatus | None = None,
    source_type: SourceType | None = None,
) -> SourceListResponse:
    with STORE.lock:
        items = [record.source for record in STORE.sources.values()]

    if source_status is not None:
        items = [item for item in items if item.source_status == source_status]

    if source_type is not None:
        items = [item for item in items if item.source_type == source_type]

    return SourceListResponse(items=[_to_summary(item) for item in items])


def get_source(source_id: UUID) -> SourceDetail | None:
    with STORE.lock:
        record = STORE.sources.get(source_id)
    if record is None:
        return None

    source = record.source
    return SourceDetail(
        id=source.id,
        source_type=source.source_type,
        source_status=source.source_status,
        original_filename=source.original_filename,
        ingested_at=source.ingested_at,
        extraction_confidence=record.extraction_confidence,
        has_raw_text=bool(source.raw_text),
    )


def reprocess_source(source_id: UUID) -> SourceSummary | None:
    with STORE.lock:
        record = STORE.sources.get(source_id)
        if record is None:
            return None

        for session_id in record.session_ids:
            STORE.sessions.pop(session_id, None)

        record.source.source_status = SourceStatus.QUEUED
        _run_ingestion_pipeline(source_id)
        return _to_summary(record.source)


def create_uploaded_source(
    *,
    source_type: SourceType,
    original_filename: str,
    content: bytes,
) -> SourceUploadResponse:
    with STORE.lock:
        source = SourceFile(
            source_type=source_type,
            original_filename=original_filename,
            source_status=SourceStatus.UPLOADED,
        )
        artifact = validate_and_store_upload(
            source_id=str(source.id),
            source_type=source_type,
            original_filename=original_filename,
            content=content,
        )
        source.details_json = {
            "source_reference": f"source://{source.id}",
            "storage_key": artifact.storage_key,
            "content_sha256": artifact.content_sha256,
            "size_bytes": artifact.size_bytes,
        }
        STORE.sources[source.id] = SourceRecord(source=source, content="")

    summary = _to_summary(source)
    return SourceUploadResponse(
        **summary.model_dump(),
        source_reference=f"source://{source.id}",
        storage_key=artifact.storage_key,
        size_bytes=artifact.size_bytes,
        content_sha256=artifact.content_sha256,
    )
