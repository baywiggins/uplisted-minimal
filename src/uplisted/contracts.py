"""Strict, provenance-carrying contracts for Uplisted state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator

from uplisted.errors import ToolError
from uplisted.state.hashing import canonical_hash

ArtifactKind = Literal["evidence", "pricing", "floorplan", "photos", "listing"]
ResourceKind = Literal["property", "evidence", "pricing", "floorplan", "photos", "listing"]
PropertyType = Literal["single_family", "townhouse", "condo", "apartment"]
RoomKind = Literal[
    "bedroom",
    "full_bathroom",
    "half_bathroom",
    "kitchen",
    "living",
    "hall",
    "stairs",
    "garage",
    "other",
]
ArtifactOrigin = Literal["scripted", "live_model", "deterministic", "human_edit"]
PayloadT = TypeVar("PayloadT", bound=BaseModel)
DataT = TypeVar("DataT")


class StrictModel(BaseModel):
    """Reject coercion and unrecognized fields at every persisted boundary."""

    model_config = ConfigDict(extra="forbid", strict=True)


class Address(StrictModel):
    street: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=2, max_length=2)
    postal_code: str = Field(min_length=5, max_length=10)
    unit: str | None = Field(default=None, max_length=50)


class RoomMeasurement(StrictModel):
    measurement_id: str = Field(min_length=1, max_length=100)
    room_key: str = Field(min_length=1, max_length=100)
    room_kind: RoomKind
    level_index: int = Field(ge=0, le=3)
    width_ft: Decimal = Field(gt=Decimal("0"), lt=Decimal("200"))
    length_ft: Decimal = Field(gt=Decimal("0"), lt=Decimal("200"))


class PropertyFacts(StrictModel):
    address: Address
    property_type: PropertyType
    bedrooms: int = Field(ge=0, le=20)
    full_bathrooms: int = Field(ge=0, le=20)
    half_bathrooms: int = Field(ge=0, le=20)
    square_feet: int | None = Field(default=None, gt=0)
    levels: int = Field(ge=1, le=4)
    has_garage: bool | None = None
    asking_rent_cents: int | None = Field(default=None, gt=0)
    layout_description: str | None = Field(default=None, max_length=4000)
    room_measurements: list[RoomMeasurement] = Field(default_factory=list, max_length=40)

    @model_validator(mode="after")
    def measurement_ids_are_unique(self) -> PropertyFacts:
        ids = [measurement.measurement_id for measurement in self.room_measurements]
        if len(ids) != len(set(ids)):
            raise ValueError("room measurement IDs must be unique")
        return self


class ResourceRef(StrictModel):
    kind: ResourceKind
    resource_id: str = Field(min_length=1, max_length=100)
    revision: int = Field(ge=1)
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")


class PropertySnapshot(StrictModel):
    case_id: str = Field(min_length=1, max_length=100)
    revision: int = Field(ge=1)
    facts: PropertyFacts
    confirmed_by: str = Field(min_length=1, max_length=100)
    confirmed_at: datetime
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    synthetic: bool

    def resource_ref(self) -> ResourceRef:
        return ResourceRef(
            kind="property",
            resource_id=self.case_id,
            revision=self.revision,
            content_hash=self.content_hash,
        )


class PublicFact(StrictModel):
    fact_id: str = Field(min_length=1, max_length=300)
    field_path: str = Field(min_length=1, max_length=200)
    value: str | int | bool | Decimal
    scope: Literal["subject"] = "subject"
    source_ref: ResourceRef
    confirmed: Literal[True] = True


class ArtifactEnvelope(StrictModel, Generic[PayloadT]):
    artifact_id: str = Field(min_length=1, max_length=100)
    case_id: str = Field(min_length=1, max_length=100)
    kind: ArtifactKind
    revision: int = Field(ge=1)
    created_at: datetime
    run_id: str | None = Field(default=None, max_length=100)
    dependencies: list[ResourceRef]
    payload: PayloadT
    content_hash: str = Field(pattern=r"^[a-f0-9]{64}$")
    origin: ArtifactOrigin


class ToolResult(StrictModel, Generic[DataT]):
    status: Literal["ok", "error"]
    data: DataT | None = None
    error: ToolError | None = None
    artifact_ref: ResourceRef | None = None
    event_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def status_matches_result(self) -> ToolResult[DataT]:
        if self.status == "ok" and (self.data is None or self.error is not None):
            raise ValueError("successful results require data and no error")
        if self.status == "error" and (
            self.data is not None or self.error is None or self.artifact_ref is not None
        ):
            raise ValueError("error results require an error and cannot create an artifact")
        return self


@dataclass(frozen=True)
class ExecutionContext:
    """Server-constructed agent context; it is absent from model tool JSON."""

    actor_id: str
    case_id: str
    run_id: str | None
    owner_id: str | None
    fence: int | None
    permissions: frozenset[str]


@dataclass(frozen=True)
class HumanContext:
    """Trusted browser-session context for human-only commands."""

    actor_id: str
    case_id: str
    permissions: frozenset[str]


def build_property_snapshot(
    *,
    case_id: str,
    facts: PropertyFacts,
    confirmed_by: str,
    confirmed_at: datetime,
    synthetic: bool,
    revision: int = 1,
) -> PropertySnapshot:
    """Create immutable snapshot metadata instead of trusting an input hash."""
    content = {
        "case_id": case_id,
        "revision": revision,
        "facts": facts,
        "confirmed_by": confirmed_by,
        "confirmed_at": confirmed_at,
        "synthetic": synthetic,
    }
    return PropertySnapshot(
        case_id=case_id,
        revision=revision,
        facts=facts,
        confirmed_by=confirmed_by,
        confirmed_at=confirmed_at,
        content_hash=canonical_hash(content),
        synthetic=synthetic,
    )


def build_public_facts(snapshot: PropertySnapshot) -> list[PublicFact]:
    """Expose confirmed subject facts only, with their immutable source reference."""
    values: list[tuple[str, str | int | bool | Decimal]] = [
        ("address.street", snapshot.facts.address.street),
        ("address.city", snapshot.facts.address.city),
        ("address.state", snapshot.facts.address.state),
        ("address.postal_code", snapshot.facts.address.postal_code),
        ("property_type", snapshot.facts.property_type),
        ("bedrooms", snapshot.facts.bedrooms),
        ("full_bathrooms", snapshot.facts.full_bathrooms),
        ("half_bathrooms", snapshot.facts.half_bathrooms),
        ("levels", snapshot.facts.levels),
    ]
    if snapshot.facts.address.unit is not None:
        values.append(("address.unit", snapshot.facts.address.unit))
    if snapshot.facts.square_feet is not None:
        values.append(("square_feet", snapshot.facts.square_feet))
    if snapshot.facts.has_garage is not None:
        values.append(("has_garage", snapshot.facts.has_garage))
    if snapshot.facts.asking_rent_cents is not None:
        values.append(("asking_rent_cents", snapshot.facts.asking_rent_cents))
    for measurement in snapshot.facts.room_measurements:
        prefix = f"room_measurements.{measurement.measurement_id}"
        values.extend(
            [
                (f"{prefix}.width_ft", measurement.width_ft),
                (f"{prefix}.length_ft", measurement.length_ft),
            ]
        )
    source_ref = snapshot.resource_ref()
    return [
        PublicFact(
            fact_id=f"{snapshot.case_id}:r{snapshot.revision}:{field_path}",
            field_path=field_path,
            value=value,
            source_ref=source_ref,
        )
        for field_path, value in values
    ]
