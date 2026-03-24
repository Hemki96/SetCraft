from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import SourceStatus, SourceType


class SourceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: SourceType
    content: str = Field(min_length=1, max_length=200_000)
    original_filename: str | None = None


class SourceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    source_type: SourceType
    source_status: SourceStatus
    original_filename: str | None = None
    ingested_at: datetime


class SourceDetail(SourceSummary):
    extraction_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    has_raw_text: bool = False


class SourceListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[SourceSummary]


class SourceUploadResponse(SourceSummary):
    model_config = ConfigDict(extra="forbid")

    source_reference: str
    storage_key: str
    size_bytes: int = Field(ge=1)
    content_sha256: str = Field(min_length=64, max_length=64)
