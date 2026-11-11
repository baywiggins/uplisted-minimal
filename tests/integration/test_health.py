"""Health-route integration coverage."""

from __future__ import annotations

from fastapi.testclient import TestClient

from uplisted.api.app import create_app


def test_health_is_ready_without_exposing_configuration() -> None:
    response = TestClient(create_app()).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "password" not in response.text.lower()
    assert "/Users/" not in response.text
