from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import ReviewDecisionType, TrainingSession


class SessionListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[TrainingSession]


class SessionUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    total_distance_m: int | None = Field(default=None, ge=0)
    duration_min: int | None = Field(default=None, ge=0)
    notes: str | None = None
    tags: list[str] | None = None


class BlockUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    block_type: str | None = None


class SetUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str | None = None
    distance_m: int | None = Field(default=None, ge=0)
    duration_sec: int | None = Field(default=None, ge=0)
    intensity_note: str | None = None
    normalized_notes: str | None = None
    tags: list[str] | None = None


class SessionReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: ReviewDecisionType
    comment: str | None = None
