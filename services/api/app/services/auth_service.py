from __future__ import annotations

from app.schemas.auth import LoginResponse, UserMeResponse


def build_login_placeholder_response() -> LoginResponse:
    return LoginResponse(
        access_token="placeholder-token",
        token_type="bearer",
        expires_in=3600,
    )


def build_auth_me_placeholder_response() -> UserMeResponse:
    return UserMeResponse(
        user_id="placeholder-user-id",
        email="coach@example.com",
        role="trainer",
    )
