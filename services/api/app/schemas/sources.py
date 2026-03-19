from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SourceType(StrEnum):
    DOCX = "docx"
    PDF = "pdf"
    TEXT = "text"


class SourceStatus(StrEnum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    NORMALIZING = "normalizing"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class SourceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: SourceType
    content: str = Field(min_length=1)
    original_filename: str | None = None


class SourceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    source_type: SourceType
    source_status: SourceStatus
    original_filename: str | None = None
    ingested_at: datetime


class SourceListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[SourceSummary]
