# Contributing

Contributions must improve reproducibility. An adapter or scenario PR should include a pinned platform version, workload definition, evidence provenance, execution instructions and expected result.

Do not submit unverifiable superlatives, universal security ratings or measured claims backed only by documentation. Security findings should be disclosed responsibly to the affected maintainer before public exploit details are added.

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m agentinfrabench.cli run scenarios/rootless-personal-workspace.json --output generated/rootless
```
