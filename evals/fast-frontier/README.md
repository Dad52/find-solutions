# Fast Frontier panel

This panel is the low-cost optimization loop for `find-solutions`. It measures the product's core claim: escape a stuck/default search space with an unusual, feasible, well-ranked route. It complements rather than replaces the broad 60-case regression suite.

## Files

- `cases.jsonl`: six deterministic headline cases and two milestone holdouts.
- `gold.jsonl`: withheld mechanism families, conditional winners, traps, and objective checks for raters.
- `headline-case-ids.txt`: fast offline panel.
- `holdout-case-ids.txt`: architecture plus live-web confirmation cases.
- `rubric.md`: route gates and metrics.

Run subjects in an isolated workspace that cannot read the evaluation repository. Never place gold, scorer notes, or competing outputs in model context.

## Fast candidate preflight

Create 12 randomized slots: six cases, current versus candidate, one repeat.

```bash
python3 scripts/build_run_matrix.py \
  --cases evals/fast-frontier/cases.jsonl \
  --case-ids evals/fast-frontier/headline-case-ids.txt \
  --conditions current candidate \
  --repeats 1 \
  --out runs/fast-frontier/preflight-plan.jsonl
```

This is a regression filter, not proof. Run the six cases with three repeats before promoting a candidate:

```bash
python3 scripts/build_run_matrix.py \
  --cases evals/fast-frontier/cases.jsonl \
  --case-ids evals/fast-frontier/headline-case-ids.txt \
  --conditions current candidate \
  --repeats 3 \
  --out runs/fast-frontier/confirmation-plan.jsonl
```

## Milestone comparison

Combine headline and holdout ID files outside the distributed fixture, then compare baseline, current, and candidate with three repeats. This produces 72 slots across eight cases. The web holdout must use the same evaluation date, timezone, network permissions, and source-freshness policy in all conditions.

Do not reuse a live-web output across conditions. If network or tool infrastructure fails, record `infrastructure-error`; do not grade it as a product failure.

## Rating and reporting

Blind `current` and `candidate` with `make_blind_pairs.py`. Raters receive both outputs, the case record, the matching private gold record, and `rubric.md`. Require a short normalized mechanism key for every counted practical-novel route. A mechanism absent from gold can count when the rater explains why it is structurally distinct and feasible.

Use at least two blinded raters for a replacement decision. Resolve material disagreements on frontier family, critical failure, or top-route correctness with a third rater. The existing aggregator accepts the new metric names and reports pair-level scores, case-clustered intervals, token dimensions, and median/P90 latency.

## Anti-overfitting

- Do not edit prompts, gold, metrics, or exclusions after seeing candidate outputs.
- Keep the two holdouts out of ordinary prompt iteration.
- Add a new regression case when a real failure reveals a missing mechanism or trap.
- Refresh surface details while preserving the causal structure when candidate behavior begins to memorize wording.
- Do not claim universality from six domains; the broad suite remains the release regression check.
