from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import SourceType


class SegmentType(StrEnum):
    BLOCK_HEADER = "block_header"
    SET_LINE = "set_line"
    FREE_TEXT = "free_text"


class ExtractionIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    segment_index: int | None = Field(default=None, ge=0)
    confidence_impact: float = Field(default=0.0, ge=0.0, le=1.0)


class ExtractedSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    segment_type: SegmentType
    confidence: float = Field(ge=0.0, le=1.0)
    source_line: int = Field(ge=1)
    issues: list[ExtractionIssue] = Field(default_factory=list)


class ExtractionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: SourceType
    raw_text: str
    segments: list[ExtractedSegment] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    issues: list[ExtractionIssue] = Field(default_factory=list)
    trace: dict[str, object] = Field(default_factory=dict)
