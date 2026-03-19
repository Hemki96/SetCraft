from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException

from app.core.config import get_settings
from app.schemas.health import DatabaseHealthResponse, HealthResponse
from app.services.health_service import (
    build_database_health_response,
    build_health_response,
    check_database_connection,
)

router = APIRouter()


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return build_health_response(get_settings())


@router.get("/db", response_model=DatabaseHealthResponse)
def get_database_health() -> DatabaseHealthResponse:
    if not check_database_connection():
        raise HTTPException(status_code=503, detail="Database unavailable")

    return build_database_health_response()
