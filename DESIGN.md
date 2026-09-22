# Engineering notes: DriftWatch — feature distribution monitoring

## Problem and flow

Reference window → frozen quantile boundaries → reference histogram → current window histogram → smoothed PSI and missing-rate delta → configurable alerts. Reference boundaries are never recomputed from the current batch, preventing the monitoring baseline from silently moving.

## Current boundaries

Univariate monitoring only. PSI thresholds are configurable heuristics, not statistical significance tests or proof of model quality loss. Correlation drift and label-based accuracy monitoring need separate checks. Demo values are seeded synthetic measurements.

## Interview walkthrough

1. Run the demo and explain each output in terms of the code.
2. Show a test that exercises a failure rather than only a successful call.
3. Trace one input through the core implementation and its stored state.
4. Explain the tradeoff made by the current storage or algorithm choice.
5. Describe what would change with 100× the data or concurrent users.
6. Make a small extension and add a regression test before using this in a resume.

## Validation

See `test_engine.py` for executable assertions and `docs/demo-output.txt` for
captured results. CI is configured but remote CI results are not assumed.
