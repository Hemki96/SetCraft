"""Database engine and session factories."""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def create_db_engine() -> Engine:
    """Create an SQLAlchemy engine from environment configuration."""

    return create_engine(
        get_settings().database_url,
        future=True,
        pool_pre_ping=True,
    )


def create_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """Create a session factory bound to the selected engine."""

    selected_engine = engine or create_db_engine()
    return sessionmaker(bind=selected_engine, autoflush=False, autocommit=False)


def ping_database(engine: Engine | None = None) -> bool:
    """Run a minimal health query against the configured database."""

    selected_engine = engine or create_db_engine()
    with selected_engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True
