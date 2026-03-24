from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import TrainingSession


class NormalizationIssueSeverity(StrEnum):
    WARNING = "warning"
    ERROR = "error"


class NormalizationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    severity: NormalizationIssueSeverity = NormalizationIssueSeverity.WARNING
    segment_index: int | None = Field(default=None, ge=0)
    block_index: int | None = Field(default=None, ge=0)
    set_index: int | None = Field(default=None, ge=0)
    confidence_impact: float = Field(default=0.0, ge=0.0, le=1.0)


class NormalizationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session: TrainingSession
    confidence: float = Field(ge=0.0, le=1.0)
    issues: list[NormalizationIssue] = Field(default_factory=list)
    trace: dict[str, object] = Field(default_factory=dict)
