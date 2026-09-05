from __future__ import annotations

from dataclasses import dataclass
from typing import Any


DIMENSION_WEIGHTS = {
    "isolation": 0.22,
    "identity_secrets": 0.18,
    "network": 0.16,
    "authority": 0.16,
    "recovery": 0.14,
    "observability": 0.08,
    "economics": 0.06,
}
PROVENANCE_FACTORS = {"measured": 1.0, "documented": 0.7, "synthetic": 0.5, "design": 0.0}
VALID_STATUS = {"pass", "partial", "fail", "unknown"}


@dataclass(frozen=True)
class Evidence:
    control: str
    dimension: str
    status: str
    provenance: str
    summary: str
    artifact: str | None = None
    source_url: str | None = None
    hard_gate: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Evidence":
        item = cls(**value)
        if item.dimension not in DIMENSION_WEIGHTS:
            raise ValueError(f"unsupported dimension: {item.dimension}")
        if item.status not in VALID_STATUS:
            raise ValueError(f"unsupported status: {item.status}")
        if item.provenance not in PROVENANCE_FACTORS:
            raise ValueError(f"unsupported provenance: {item.provenance}")
        if item.provenance == "documented" and not item.source_url:
            raise ValueError("documented evidence requires source_url")
        if item.provenance == "measured" and not item.artifact:
            raise ValueError("measured evidence requires artifact")
        return item


@dataclass(frozen=True)
class Economics:
    accepted_outcomes: int
    infrastructure_usd: float
    model_usd: float
    storage_network_usd: float
    observability_usd: float
    human_review_hours: float
    human_hourly_usd: float
    operations_usd: float

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Economics":
        item = cls(**value)
        if item.accepted_outcomes <= 0:
            raise ValueError("accepted_outcomes must be positive")
        if any(number < 0 for number in value.values()):
            raise ValueError("economics values cannot be negative")
        return item


@dataclass(frozen=True)
class Scenario:
    platform: str
    version: str
    workload: str
    operator: str
    run_at: str
    evidence: tuple[Evidence, ...]
    economics: Economics

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Scenario":
        required = {"platform", "version", "workload", "operator", "run_at", "evidence", "economics"}
        missing = required - value.keys()
        if missing:
            raise ValueError(f"missing fields: {', '.join(sorted(missing))}")
        return cls(
            platform=value["platform"], version=value["version"], workload=value["workload"],
            operator=value["operator"], run_at=value["run_at"],
            evidence=tuple(Evidence.from_dict(item) for item in value["evidence"]),
            economics=Economics.from_dict(value["economics"]),
        )
