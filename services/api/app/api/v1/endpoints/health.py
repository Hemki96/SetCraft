from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse
from app.services.health_service import build_health_response

router = APIRouter()


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return build_health_response(get_settings())
