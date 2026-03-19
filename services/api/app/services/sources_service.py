from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.schemas.sources import (
    SourceCreateRequest,
    SourceListResponse,
    SourceStatus,
    SourceSummary,
    SourceType,
)

_SOURCE_STORE: dict[UUID, SourceSummary] = {}


def create_source_placeholder(payload: SourceCreateRequest) -> SourceSummary:
    summary = SourceSummary(
        id=uuid4(),
        source_type=payload.source_type,
        source_status=SourceStatus.UPLOADED,
        original_filename=payload.original_filename,
        ingested_at=datetime.now(UTC),
    )
    _SOURCE_STORE[summary.id] = summary
    return summary


def list_sources_placeholder(
    *,
    source_status: SourceStatus | None = None,
    source_type: SourceType | None = None,
) -> SourceListResponse:
    items = list(_SOURCE_STORE.values())

    if source_status is not None:
        items = [item for item in items if item.source_status == source_status]

    if source_type is not None:
        items = [item for item in items if item.source_type == source_type]

    return SourceListResponse(items=items)


def get_source_placeholder(source_id: UUID) -> SourceSummary | None:
    return _SOURCE_STORE.get(source_id)


def reprocess_source_placeholder(source_id: UUID) -> SourceSummary | None:
    source = _SOURCE_STORE.get(source_id)
    if source is None:
        return None

    updated = source.model_copy(update={"source_status": SourceStatus.QUEUED})
    _SOURCE_STORE[source_id] = updated
    return updated
