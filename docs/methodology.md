# Benchmark methodology

## Rules

1. Hard safety gates override aggregate scores.
2. Evidence strength changes score contribution: measured 100%, documented 70%, synthetic 50%, design 0%.
3. Missing dimensions score zero; absence of evidence is not evidence of control failure, but it cannot support readiness.
4. Platform maintainers may challenge facts through reproducible evidence and source corrections.
5. Comparisons must use the same workload contract, version window and acceptance test.
6. Costs include infrastructure, models, storage/network, observability, human review and operations.

## Workload-specific verdicts

A result is never a universal platform rating. A shared-kernel container may be appropriate for one trusted developer while being ineligible for hostile multitenancy. Every score names its workload.

## Publication checklist

- Pin platform and adapter versions.
- Name the operator and timestamp.
- Preserve raw artifacts and hashes.
- Document network, region, machine type and model.
- Repeat runs and publish variance for performance claims.
- Separate documentation assessment from execution.
- Give vendors a correction path.
