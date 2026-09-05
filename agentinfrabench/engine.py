from __future__ import annotations

import hashlib
import json
from dataclasses import asdict

from .model import DIMENSION_WEIGHTS, PROVENANCE_FACTORS, Evidence, Scenario


STATUS_POINTS = {"pass": 100.0, "partial": 50.0, "fail": 0.0, "unknown": 0.0}


def _dimension_scores(evidence: tuple[Evidence, ...]) -> dict[str, float]:
    result: dict[str, float] = {}
    for dimension in DIMENSION_WEIGHTS:
        items = [item for item in evidence if item.dimension == dimension]
        if not items:
            result[dimension] = 0.0
            continue
        points = [STATUS_POINTS[item.status] * PROVENANCE_FACTORS[item.provenance] for item in items]
        result[dimension] = round(sum(points) / len(points), 2)
    return result


def evaluate(scenario: Scenario) -> dict:
    scores = _dimension_scores(scenario.evidence)
    total = round(sum(scores[key] * weight for key, weight in DIMENSION_WEIGHTS.items()), 2)
    hard_failures = [item for item in scenario.evidence if item.hard_gate and item.status != "pass"]
    design_items = [item for item in scenario.evidence if item.provenance == "design"]
    economics = scenario.economics
    fully_loaded = round(
        economics.infrastructure_usd + economics.model_usd + economics.storage_network_usd
        + economics.observability_usd + economics.human_review_hours * economics.human_hourly_usd
        + economics.operations_usd, 4
    )
    unit_cost = round(fully_loaded / economics.accepted_outcomes, 6)
    if hard_failures:
        verdict = "not_eligible"
    elif design_items:
        verdict = "design_only"
    elif total >= 80:
        verdict = "production_candidate"
    elif total >= 60:
        verdict = "conditional"
    else:
        verdict = "development_only"
    payload = {
        "schema_version": "1.0.0", "platform": scenario.platform, "platform_version": scenario.version,
        "workload": scenario.workload, "operator": scenario.operator, "run_at": scenario.run_at,
        "verdict": verdict, "score": total, "dimension_scores": scores,
        "hard_gate_failures": [item.control for item in hard_failures],
        "design_only_controls": [item.control for item in design_items],
        "fully_loaded_cost_usd": fully_loaded, "accepted_outcomes": economics.accepted_outcomes,
        "cost_per_accepted_outcome_usd": unit_cost,
        "evidence_summary": {
            provenance: sum(1 for item in scenario.evidence if item.provenance == provenance)
            for provenance in PROVENANCE_FACTORS
        },
        "findings": [asdict(item) for item in scenario.evidence if item.status in {"fail", "partial", "unknown"}],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload
