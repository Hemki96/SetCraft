from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from training_plan_schemas.domain_v1 import TrainingSession


class RetrievalSearchMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session: TrainingSession
    structured_score: float
    semantic_score: float
    combined_score: float
    matched_fields: list[str]


class RetrievalSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[TrainingSession]
    matches: list[RetrievalSearchMatch] = Field(default_factory=list)
    semantic_enabled: bool = True
