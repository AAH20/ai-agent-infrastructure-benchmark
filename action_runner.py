from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agentinfrabench.engine import evaluate
from agentinfrabench.model import Scenario
from agentinfrabench.render import write_outputs


scenario = Scenario.from_dict(json.loads(Path(sys.argv[1]).read_text()))
result = evaluate(scenario)
write_outputs(result, Path(sys.argv[2]))
print(f"AgentInfraBench verdict={result['verdict']} score={result['score']}")
raise SystemExit(2 if result["verdict"] == "not_eligible" else 0)
