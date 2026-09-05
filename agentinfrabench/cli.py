from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import evaluate
from .model import Scenario
from .render import write_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark AI agent infrastructure")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("scenario", type=Path)
    run.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scenario = Scenario.from_dict(json.loads(args.scenario.read_text()))
    result = evaluate(scenario)
    write_outputs(result, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["verdict"] == "not_eligible" else 0


if __name__ == "__main__":
    raise SystemExit(main())
