# Fast Frontier rubric

Use this panel to test whether a candidate finds **unusual routes that remain usable**. Do not reward prose length, idea count, citations, or novelty by itself. The subject under evaluation receives only the case prompt and normal runtime context; never expose `gold.jsonl`, rater notes, or another condition's output.

## Route acceptance gate

Count a route only when all are true:

1. it honors every hard constraint and does not repeat a rejected attempt;
2. it names a causal mechanism and concrete intervention object, not just a technique label;
3. the first action is feasible with the stated owner, access, time, and resources;
4. it names an observable result and a continue/stop, rollback, or fallback decision;
5. it is not a cosmetic or provider variant of another counted route.

An equivalent mechanism absent from `gold.jsonl` may count. The rater must record its normalized key and one sentence explaining equivalence or novelty; gold is a floor, not an exhaustive answer key.

## Primary metrics

- **frontier_success_at_3 (`0|1`)**: at least one of the first three routes passes the acceptance gate, avoids the default families, and matches a frontier family or an equally strong decision-distinct mechanism.
- **practical_novelty_at_5 (`0..5`)**: accepted frontier mechanisms among the first five. Novel but infeasible ideas score zero.
- **accepted_route_at_5 (`0..5`)**: accepted routes among the first five.
- **ranking_hit_at_1 (`0|1`)**: the first route is the correct conditional winner for the facts given, or the cheapest discriminator when the winner cannot yet be known.
- **trap_count_at_5 (`0..5`)**: top-five routes that hit a declared trap. Lower is better. `trap_rate_at_5 = trap_count / min(5, presented_routes)`.

## Diagnostic metrics

- **unique_mechanism_at_5 (`0..5`)**: unique accepted mechanism keys among the first five.
- **duplicate_rate_at_5**: `1 - unique_mechanism / max(1, accepted_route)`.
- **route_package_completeness (`0..4`)**: `0` no executable package; `1` action; `2` action + signal; `3` adds stop/rollback; `4` adds a material fallback and evidence boundary.
- **constraint_fit (`0..4`)**, **evidence_calibration (`0..4`)**, and **clarity_efficiency (`0..4`)** retain the definitions in the main rubric.
- **padding_failure (`0|1`)**: the narrow control adds multiple solution families or unnecessary research after the exact correction is established.

## Critical failure

Mark a critical failure if the output violates a hard constraint, invents current facts or external actions, crosses a safety boundary, or drifts to another outcome. A critical failure cannot win the pair regardless of novelty.

## Pair preference

Prefer the output more likely to produce the correct next decision. Apply this order:

1. no critical failure;
2. frontier success and ranking hit;
3. more accepted practical novelty and unique mechanisms;
4. fewer traps and duplicates;
5. stronger route packages;
6. lower tokens and wall time when decision quality is otherwise equivalent.

Do not collapse the panel into one pseudo-precise quality percentage. Report axes and paired differences separately.

## Efficiency

Record input, cached input, reasoning, output, and total tokens separately when the host exposes them. Report tool calls plus median and P90 wall time. Useful diagnostics include:

- `accepted_route_at_5 / output_tokens * 1000`;
- `practical_novelty_at_5 / total_tokens * 1000`;
- critical failures and infrastructure errors as counts, never as zero-quality model outputs.

## Suggested decision guardrails

For a fast one-repeat preflight, treat results as directional only. Promote a candidate to repeated testing when it has zero new critical failures, does not reduce accepted routes materially, improves frontier success or practical novelty on at least two cases, and does not increase median tokens or P90 latency by more than 20% without an explicit quality trade.

For a replacement decision, use at least three paired repeats and the two holdouts. Require no hard-constraint regression, report the paired case-clustered interval, and disclose any domain where the candidate regresses.
