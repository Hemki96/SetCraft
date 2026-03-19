from __future__ import annotations

from fastapi import APIRouter

from app.schemas.auth import LoginRequest, LoginResponse, UserMeResponse
from app.services.auth_service import (
    build_auth_me_placeholder_response,
    build_login_placeholder_response,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    del payload
    return build_login_placeholder_response()


@router.get("/me", response_model=UserMeResponse)
def auth_me() -> UserMeResponse:
    return build_auth_me_placeholder_response()
