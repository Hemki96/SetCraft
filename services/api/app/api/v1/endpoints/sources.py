from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException

from app.schemas.sources import (
    SourceCreateRequest,
    SourceDetail,
    SourceListResponse,
    SourceStatus,
    SourceSummary,
    SourceType,
    SourceUploadResponse,
)
from app.services.sources_service import (
    create_source,
    create_uploaded_source,
    get_source,
    list_sources,
    reprocess_source,
)
from app.services.upload_service import UploadValidationError

router = APIRouter()


@router.post("", response_model=SourceSummary)
def create_source_endpoint(payload: SourceCreateRequest) -> SourceSummary:
    return create_source(payload)


@router.post("/upload", response_model=SourceUploadResponse)
def upload_source_endpoint(
    source_type: SourceType,
    original_filename: str,
    content: bytes = Body(..., media_type="application/octet-stream"),
) -> SourceUploadResponse:
    try:
        return create_uploaded_source(
            source_type=source_type,
            original_filename=original_filename,
            content=content,
        )
    except UploadValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=SourceListResponse)
def list_sources_endpoint(
    source_status: SourceStatus | None = None,
    source_type: SourceType | None = None,
) -> SourceListResponse:
    return list_sources(
        source_status=source_status,
        source_type=source_type,
    )


@router.get("/{source_id}", response_model=SourceDetail)
def get_source_endpoint(source_id: UUID) -> SourceDetail:
    source = get_source(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("/{source_id}/reprocess", response_model=SourceSummary)
def reprocess_source_endpoint(source_id: UUID) -> SourceSummary:
    source = reprocess_source(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source
