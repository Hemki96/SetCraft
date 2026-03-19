from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from training_plan_schemas.domain_v1 import TrainingSession


class RetrievalSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[TrainingSession]
