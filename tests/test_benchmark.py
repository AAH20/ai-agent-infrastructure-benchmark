import json
import tempfile
import unittest
from pathlib import Path

from agentinfrabench.engine import evaluate
from agentinfrabench.model import Evidence, Scenario
from agentinfrabench.render import write_outputs


ROOT = Path(__file__).parents[1]


def scenario(name):
    return Scenario.from_dict(json.loads((ROOT / "scenarios" / name).read_text()))


class BenchmarkTests(unittest.TestCase):
    def test_documented_hard_failures_override_score(self):
        result = evaluate(scenario("remote-futrx-documented.json"))
        self.assertEqual(result["verdict"], "not_eligible")
        self.assertIn("isolation.host_execution", result["hard_gate_failures"])

    def test_design_controls_cannot_create_production_claim(self):
        result = evaluate(scenario("agentfabric-reference.json"))
        self.assertEqual(result["verdict"], "design_only")
        self.assertGreater(len(result["design_only_controls"]), 0)

    def test_unit_cost_includes_human_review(self):
        result = evaluate(scenario("rootless-personal-workspace.json"))
        self.assertEqual(result["fully_loaded_cost_usd"], 528.2)
        self.assertEqual(result["cost_per_accepted_outcome_usd"], 4.401667)

    def test_documented_evidence_requires_source(self):
        with self.assertRaises(ValueError):
            Evidence.from_dict({"control":"x","dimension":"network","status":"pass","provenance":"documented","summary":"x"})

    def test_measured_evidence_requires_artifact(self):
        with self.assertRaises(ValueError):
            Evidence.from_dict({"control":"x","dimension":"network","status":"pass","provenance":"measured","summary":"x"})

    def test_all_output_formats_are_created(self):
        result = evaluate(scenario("rootless-personal-workspace.json"))
        with tempfile.TemporaryDirectory() as directory:
            write_outputs(result, Path(directory))
            self.assertEqual({"result.json", "scorecard.md", "results.sarif", "junit.xml"}, {path.name for path in Path(directory).iterdir()})

    def test_receipt_is_deterministic(self):
        self.assertEqual(evaluate(scenario("rootless-personal-workspace.json"))["receipt_sha256"], evaluate(scenario("rootless-personal-workspace.json"))["receipt_sha256"])


if __name__ == "__main__":
    unittest.main()
