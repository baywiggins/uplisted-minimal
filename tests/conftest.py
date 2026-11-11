"""Test-wide network boundary for offline backend checks."""

from __future__ import annotations

import os
import socket
from collections.abc import Generator
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def block_external_sockets(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Permit loopback only; offline tests must not reach external services."""
    allowed_hosts = {"127.0.0.1", "::1", "localhost"}
    allowed_port = int(os.environ.get("PGPORT", "5433"))
    original_connect = socket.socket.connect
    original_create_connection = socket.create_connection

    def allow(address: Any) -> bool:
        if isinstance(address, str):
            return True
        return (
            isinstance(address, tuple)
            and len(address) >= 2
            and address[0] in allowed_hosts
            and address[1] == allowed_port
        )

    def guarded_connect(sock: socket.socket, address: Any) -> Any:
        if not allow(address):
            raise RuntimeError(f"External network blocked during tests: {address!r}")
        return original_connect(sock, address)

    def guarded_create_connection(address: Any, *args: Any, **kwargs: Any) -> socket.socket:
        if not allow(address):
            raise RuntimeError(f"External network blocked during tests: {address!r}")
        return original_create_connection(address, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket, "create_connection", guarded_create_connection)
    yield
