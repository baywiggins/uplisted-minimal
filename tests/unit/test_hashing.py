"""Canonical hash behavior tests."""

from __future__ import annotations

from datetime import datetime

import pytest

from uplisted.state.hashing import canonical_hash


def test_dictionary_order_does_not_change_a_hash() -> None:
    assert canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2})


def test_values_and_list_order_change_a_hash() -> None:
    assert canonical_hash({"items": [1, 2]}) != canonical_hash({"items": [2, 1]})
    assert canonical_hash({"value": 1}) != canonical_hash({"value": 2})


def test_canonical_hash_normalizes_utc_timestamps() -> None:
    assert canonical_hash({"at": datetime.fromisoformat("2026-11-07T12:00:00+00:00")}) == canonical_hash(
        {"at": datetime.fromisoformat("2026-11-07T07:00:00-05:00")}
    )


def test_canonical_hash_rejects_float_values() -> None:
    with pytest.raises(TypeError, match="floats"):
        canonical_hash({"rent": 1.5})
