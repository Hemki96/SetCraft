from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ExportFormat(StrEnum):
    JSON = "json"
    TXT = "txt"


class ExportStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ExportCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_plan_id: UUID
    export_format: ExportFormat = ExportFormat.JSON


class ExportJobResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    generated_plan_id: UUID
    export_format: ExportFormat
    status: ExportStatus
    file_name: str | None = None
    created_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None
