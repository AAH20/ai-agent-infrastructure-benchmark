from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


def write_outputs(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    rows = "\n".join(f"| {key.replace('_', ' ').title()} | {value:.2f} |" for key, value in result["dimension_scores"].items())
    gates = ", ".join(result["hard_gate_failures"]) or "None"
    scorecard = f"""# AgentInfraBench scorecard

| Field | Result |
|---|---|
| Platform | {result['platform']} {result['platform_version']} |
| Workload | {result['workload']} |
| Verdict | **{result['verdict']}** |
| Weighted score | **{result['score']:.2f}/100** |
| Cost per accepted outcome | **${result['cost_per_accepted_outcome_usd']:.6f}** |
| Hard-gate failures | {gates} |
| Evidence receipt | `{result['receipt_sha256']}` |

## Dimensions

| Dimension | Evidence-adjusted score |
|---|---:|
{rows}

## Evidence boundary

Provenance counts: `{json.dumps(result['evidence_summary'], sort_keys=True)}`. Documented, synthetic and design evidence must not be represented as independently measured production evidence.
"""
    (output / "scorecard.md").write_text(scorecard)
    _write_sarif(result, output / "results.sarif")
    _write_junit(result, output / "junit.xml")


def _write_sarif(result: dict, destination: Path) -> None:
    findings = []
    for item in result["findings"]:
        findings.append({
            "ruleId": item["control"],
            "level": "error" if item["hard_gate"] or item["status"] == "fail" else "warning",
            "message": {"text": f"{item['summary']} [provenance={item['provenance']}]"},
        })
    sarif = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [{"tool": {"driver": {"name": "AgentInfraBench", "rules": []}}, "results": findings}]}
    destination.write_text(json.dumps(sarif, indent=2, sort_keys=True) + "\n")


def _write_junit(result: dict, destination: Path) -> None:
    failures = result["hard_gate_failures"]
    suite = ET.Element("testsuite", name="AgentInfraBench hard gates", tests=str(max(1, len(failures))), failures=str(len(failures)))
    if failures:
        for control in failures:
            case = ET.SubElement(suite, "testcase", name=control)
            ET.SubElement(case, "failure", message="hard safety gate failed").text = control
    else:
        ET.SubElement(suite, "testcase", name="hard-gates")
    ET.ElementTree(suite).write(destination, encoding="unicode", xml_declaration=True)
