from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import GeneratedPlan, ValidationResult


class GenerateSetPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_session_ids: list[UUID] = Field(default_factory=list)
    target_distance_m: int | None = Field(default=None, ge=0)
    focus_tags: list[str] = Field(default_factory=list)


class GenerateSessionPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_session_ids: list[UUID] = Field(default_factory=list)
    target_distance_m: int | None = Field(default=None, ge=0)
    target_duration_min: int | None = Field(default=None, ge=0)
    focus_tags: list[str] = Field(default_factory=list)


class GenerateWeekPlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_session_ids: list[UUID] = Field(default_factory=list)
    sessions_per_week: int = Field(default=4, ge=1, le=14)
    target_total_distance_m: int | None = Field(default=None, ge=0)
    focus_tags: list[str] = Field(default_factory=list)


class GeneratedPlanDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan: GeneratedPlan
    validation_results: list[ValidationResult]


class GenerationApprovalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan: GeneratedPlan
    approved: bool
    validation_results: list[ValidationResult]
