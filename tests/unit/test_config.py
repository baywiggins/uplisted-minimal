"""Configuration safety tests."""

from __future__ import annotations

import socket

import pytest
from pydantic import ValidationError

from uplisted.config import Settings


def test_settings_default_to_scripted_fixture_mode() -> None:
    settings = Settings()

    assert settings.app_env == "local"
    assert settings.model_mode == "scripted"
    assert settings.rentcast_mode == "fixture"
    assert settings.auth_mode == "local_demo"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_mode", "pretend"),
        ("rentcast_mode", "cached"),
        ("app_env", "staging"),
        ("pgport", 0),
    ],
)
def test_settings_reject_invalid_values(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value})


def test_external_network_is_blocked() -> None:
    with pytest.raises(RuntimeError, match="External network blocked"):
        socket.create_connection(("example.com", 443), timeout=0.01)
