from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.auth import LoginRequest, LoginResponse, UserMeResponse
from app.services.audit_service import record_audit_event
from app.services.auth_service import (
    RequestActor,
    build_auth_me_placeholder_response,
    build_login_placeholder_response,
    get_request_actor,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    response = build_login_placeholder_response()
    actor = RequestActor(user_id=payload.email, role=response.role)
    record_audit_event(
        event_type="auth",
        action="login",
        outcome="success",
        actor=actor,
        entity_type="user",
        entity_id=payload.email,
        message="User login accepted",
    )
    return response


@router.get("/me", response_model=UserMeResponse)
def auth_me(actor: RequestActor = Depends(get_request_actor)) -> UserMeResponse:
    return build_auth_me_placeholder_response(actor)
