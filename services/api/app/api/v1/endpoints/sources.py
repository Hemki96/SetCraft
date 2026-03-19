from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.schemas.sources import (
    SourceCreateRequest,
    SourceListResponse,
    SourceStatus,
    SourceSummary,
    SourceType,
)
from app.services.sources_service import (
    create_source_placeholder,
    get_source_placeholder,
    list_sources_placeholder,
    reprocess_source_placeholder,
)

router = APIRouter()


@router.post("", response_model=SourceSummary)
def create_source(payload: SourceCreateRequest) -> SourceSummary:
    return create_source_placeholder(payload)


@router.get("", response_model=SourceListResponse)
def list_sources(
    source_status: SourceStatus | None = None,
    source_type: SourceType | None = None,
) -> SourceListResponse:
    return list_sources_placeholder(
        source_status=source_status,
        source_type=source_type,
    )


@router.get("/{source_id}", response_model=SourceSummary)
def get_source(source_id: UUID) -> SourceSummary:
    source = get_source_placeholder(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("/{source_id}/reprocess", response_model=SourceSummary)
def reprocess_source(source_id: UUID) -> SourceSummary:
    source = reprocess_source_placeholder(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source
