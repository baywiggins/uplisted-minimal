"""Canonical content hashing independent of database JSON representation."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


def canonical_hash(value: BaseModel | dict[str, Any]) -> str:
    """Hash canonical UTF-8 JSON while rejecting ambiguous float values."""
    normalized = _normalize(value.model_dump(mode="python") if isinstance(value, BaseModel) else value)
    encoded = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalize(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _normalize(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("canonical timestamps must include a timezone")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, float):
        raise TypeError("floats are not permitted in canonical values")
    if isinstance(value, str | int | bool) or value is None:
        return value
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")
