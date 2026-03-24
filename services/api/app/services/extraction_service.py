from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import SourceType


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_text: str
    segments: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


def extract_text(*, source_type: SourceType, content: str) -> ExtractionResult:
    normalized = content.strip()
    segments = [line.strip() for line in normalized.splitlines() if line.strip()]
    if not segments:
        segments = [normalized]

    confidence = 0.95 if source_type == SourceType.TEXT else 0.7

    return ExtractionResult(
        raw_text=normalized,
        segments=segments,
        confidence=confidence,
    )
