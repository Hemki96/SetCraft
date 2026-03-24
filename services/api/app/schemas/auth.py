from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class UserRole(StrEnum):
    ADMIN = "admin"
    TRAINER = "trainer"


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str
    expires_in: int = Field(ge=1)
    role: UserRole


class UserMeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    email: str
    role: UserRole
