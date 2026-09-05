# Platform adapters

An adapter prepares a pinned platform version, executes workload probes and emits a scenario document. It must not calculate its own score.

Adapter requirements:

- fail if platform-version detection is unavailable;
- write raw evidence before normalized observations;
- redact credentials without destroying provenance;
- distinguish measured facts from documentation and simulation;
- avoid destructive or escape testing unless the operator explicitly selected an isolated test environment;
- never target infrastructure outside the declared benchmark scope.

The `example` manifest documents the initial portable contract. Runtime-specific collectors are the next implementation milestone.
