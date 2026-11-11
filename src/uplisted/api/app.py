"""Application factory for the local and Azure hosting targets."""

from __future__ import annotations

from fastapi import FastAPI

from uplisted.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the HTTP application without starting any provider work."""
    app_settings = settings or Settings()
    app = FastAPI(title="Uplisted", version="0.1.0")
    app.state.settings = app_settings

    @app.get("/api/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
