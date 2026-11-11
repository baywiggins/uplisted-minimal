"""Fixture-safe application configuration."""

from __future__ import annotations

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated configuration that defaults to non-billable local providers."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["local", "azure"] = "local"
    model_mode: Literal["scripted", "live"] = "scripted"
    model_provider: Literal["azure_openai"] = "azure_openai"
    rentcast_mode: Literal["fixture", "live"] = "fixture"
    auth_mode: Literal["local_demo", "entra"] = "local_demo"
    case_id: str = "case-a"
    app_origin: str = "http://127.0.0.1:5173"

    db_auth_mode: Literal["local_password", "entra"] = "local_password"
    pghost: str = "127.0.0.1"
    pgport: int = Field(default=5433, ge=1, le=65535)
    pgdatabase: str = "uplisted"
    pguser: str = "uplisted_dev"
    pgpassword: str = "local-demo-only"
    pgsslmode: Literal["disable", "require", "verify-full"] = "disable"

    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""
    azure_tenant_id: str = ""
    azure_subscription_id: str = ""
    azure_client_id: str = ""
    azure_ai_project_endpoint: str = ""
    rentcast_api_key: str = ""
    applicationinsights_connection_string: str = ""
