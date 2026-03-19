from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.retrieval import router as retrieval_router
from app.api.v1.endpoints.sessions import router as sessions_router
from app.api.v1.endpoints.sources import router as sources_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(health_router, prefix="/health", tags=["health"])
v1_router.include_router(sources_router, prefix="/sources", tags=["sources"])
v1_router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
v1_router.include_router(retrieval_router, prefix="/retrieval", tags=["retrieval"])
