from __future__ import annotations

from functools import lru_cache
import os

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    service_name: str = Field(default="setcraft-api")
    api_version: str = Field(default="v1")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    postgres_db: str = Field(default="training_plan_platform")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    database_url: str


def _build_database_url() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "training_plan_platform")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        service_name=os.getenv("APP_NAME", "setcraft-api"),
        api_version=os.getenv("API_VERSION", "v1"),
        environment=os.getenv("APP_ENV", "development"),
        debug=os.getenv("APP_DEBUG", "false").lower() == "true",
        postgres_db=os.getenv("POSTGRES_DB", "training_plan_platform"),
        postgres_user=os.getenv("POSTGRES_USER", "postgres"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        database_url=_build_database_url(),
    )
