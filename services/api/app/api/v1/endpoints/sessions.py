from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from training_plan_schemas.domain_v1 import TrainingSession

from app.schemas.sessions import SessionListResponse
from app.services.sessions_service import get_session_placeholder, list_sessions_placeholder

router = APIRouter()


@router.get("", response_model=SessionListResponse)
def list_sessions() -> SessionListResponse:
    return list_sessions_placeholder()


@router.get("/{session_id}", response_model=TrainingSession)
def get_session(session_id: UUID) -> TrainingSession:
    session = get_session_placeholder(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
