from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="ok")
    service: str
    version: str
    environment: str


class DatabaseHealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = Field(default="ok")
    database: str = Field(default="ok")
