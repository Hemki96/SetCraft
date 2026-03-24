from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Header, HTTPException

from app.schemas.auth import LoginResponse, UserMeResponse, UserRole


@dataclass(frozen=True)
class RequestActor:
    user_id: str
    role: UserRole


def get_request_actor(
    x_user_id: Annotated[str | None, Header(alias="x-user-id")] = None,
    x_user_role: Annotated[UserRole, Header(alias="x-user-role")] = UserRole.TRAINER,
) -> RequestActor:
    return RequestActor(
        user_id=x_user_id or "placeholder-user-id",
        role=x_user_role,
    )


def require_role(*, actor: RequestActor, allowed_roles: set[UserRole], action: str) -> None:
    if actor.role in allowed_roles:
        return
    allowed = ", ".join(role.value for role in sorted(allowed_roles, key=lambda item: item.value))
    raise HTTPException(
        status_code=403,
        detail=f"Action '{action}' requires one of these roles: {allowed}.",
    )


def build_login_placeholder_response() -> LoginResponse:
    return LoginResponse(
        access_token="placeholder-token",
        token_type="bearer",
        expires_in=3600,
        role=UserRole.TRAINER,
    )


def build_auth_me_placeholder_response(actor: RequestActor) -> UserMeResponse:
    return UserMeResponse(
        user_id=actor.user_id,
        email="coach@example.com",
        role=actor.role,
    )
