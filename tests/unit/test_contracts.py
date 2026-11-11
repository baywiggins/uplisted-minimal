"""Strict contract and provenance tests."""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from uplisted.contracts import (
    ArtifactEnvelope,
    PropertyFacts,
    ResourceRef,
    RoomMeasurement,
    ToolResult,
    build_property_snapshot,
    build_public_facts,
)
from uplisted.errors import ToolError

FIXTURES = Path(__file__).parents[2] / "fixtures"


def property_facts() -> PropertyFacts:
    fixture = json.loads((FIXTURES / "property-case.json").read_text())
    return PropertyFacts.model_validate(fixture["facts"])


def test_positive_property_fixture_is_strictly_valid() -> None:
    facts = property_facts()

    assert facts.has_garage is False
    assert facts.asking_rent_cents is None
    assert facts.full_bathrooms + facts.half_bathrooms == 3


@pytest.mark.parametrize(
    "filename",
    ["negative-property-string-bedroom.json", "negative-property-unknown-field.json"],
)
def test_negative_fixtures_fail_at_the_boundary(filename: str) -> None:
    with pytest.raises(ValidationError):
        PropertyFacts.model_validate_json((FIXTURES / filename).read_text())


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("bedrooms", True),
        ("asking_rent_cents", -1),
        ("levels", 5),
        ("has_garage", "false"),
    ],
)
def test_property_facts_reject_coercion_and_invalid_ranges(field: str, value: object) -> None:
    data = property_facts().model_dump()
    data[field] = value

    with pytest.raises(ValidationError):
        PropertyFacts.model_validate(data)


def test_room_measurements_require_unique_ids_and_confirmed_dimensions() -> None:
    measurement = RoomMeasurement(
        measurement_id="kitchen-1",
        room_key="kitchen",
        room_kind="kitchen",
        level_index=0,
        width_ft=Decimal("10"),
        length_ft=Decimal("12"),
    )
    data = property_facts().model_dump()
    data["room_measurements"] = [measurement.model_dump(), measurement.model_dump()]

    with pytest.raises(ValidationError, match="unique"):
        PropertyFacts.model_validate(data)


def test_public_facts_are_subject_only_and_keep_false_distinct_from_unknown() -> None:
    facts = property_facts()
    snapshot = build_property_snapshot(
        case_id="case-a",
        facts=facts,
        confirmed_by="demo-human",
        confirmed_at=datetime.fromisoformat("2026-11-07T12:00:00+00:00"),
        synthetic=True,
    )
    public_facts = build_public_facts(snapshot)
    values = {fact.field_path: fact.value for fact in public_facts}

    assert values["has_garage"] is False
    assert "asking_rent_cents" not in values
    assert all(fact.source_ref == snapshot.resource_ref() for fact in public_facts)
    assert all(fact.scope == "subject" and fact.confirmed for fact in public_facts)


def test_tool_results_require_exactly_one_success_or_error_shape() -> None:
    error = ToolError(code="validation_failed", message="Invalid tool input", retryable=False)

    with pytest.raises(ValidationError):
        ToolResult[dict[str, str]](status="ok", data=None)
    with pytest.raises(ValidationError):
        ToolResult[dict[str, str]](status="error", data={"value": "wrong"}, error=error)
    with pytest.raises(ValidationError):
        ToolResult[dict[str, str]](status="error", error=error, artifact_ref=sample_ref())


def sample_ref() -> ResourceRef:
    return ResourceRef(kind="property", resource_id="case-a", revision=1, content_hash="a" * 64)


class ExamplePayload(BaseModel):
    label: str


def test_artifact_envelope_carries_immutable_dependency_refs() -> None:
    envelope = ArtifactEnvelope[ExamplePayload](
        artifact_id="listing-a",
        case_id="case-a",
        kind="listing",
        revision=1,
        created_at=datetime.fromisoformat("2026-11-07T12:00:00+00:00"),
        dependencies=[sample_ref()],
        payload=ExamplePayload(label="fixture"),
        content_hash="b" * 64,
        origin="scripted",
    )

    assert envelope.dependencies == [sample_ref()]
