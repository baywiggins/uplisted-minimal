"""Typed errors shared by domain and transport boundaries."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ErrorCode = Literal[
    "needs_clarification",
    "input_stale",
    "evidence_insufficient",
    "provider_disabled",
    "provider_unavailable",
    "provider_outcome_unknown",
    "validation_failed",
    "forbidden",
    "budget_exhausted",
    "cancelled",
    "idempotency_conflict",
    "run_active",
    "not_found",
]


class ToolError(BaseModel):
    """A redacted, typed failure safe to return through a tool boundary."""

    model_config = ConfigDict(extra="forbid", strict=True)

    code: ErrorCode
    message: str = Field(min_length=1, max_length=500)
    retryable: bool
    details: dict[str, Any] = Field(default_factory=dict)


class DomainError(Exception):
    """A domain failure that adapters convert to a ``ToolResult`` envelope."""

    def __init__(self, error: ToolError) -> None:
        self.error = error
        super().__init__(error.message)
