# Evaluation

`find-solutions` v0.1.0 ships an evaluation protocol, not a completed performance claim. The suite is designed to test whether the skill changes a user's decision, not whether it generates a longer answer.

## Compare two conditions

Hold the host, model snapshot, reasoning setting, tool permissions, location/time context, and source freshness constant:

- `baseline`: no `find-solutions` skill;
- `release`: the immutable v0.1.0 release.

An optional `adhd` comparator is valid only for the declared overlap set in `competitor-case-ids.txt`. Do not treat a non-overlapping task as a failure of either product.

Use at least five independent repeats per case. Record the exact prompt, host/model, tools, input/output tokens, wall time, and failures. Randomize condition order to reduce cache and time effects.

## Metrics

1. **usable_route@5** — routes among the first five that fit the constraints, use distinct mechanisms, are executable, and do not repeat an attempted route.
2. **recovery_success@3** — whether one of the first three gives a credible way around the stated blocker.

Blinded human or strong independent judging is required for both. Supporting diagnostics include constraint violations, duplicate mechanisms, unsupported current claims, evidence calibration, fallback quality, token use, wall time, and explicit-invocation precision.

## Run a smoke comparison

A 12-case smoke pass with three repeats across two conditions creates 72 runs. The 60-case suite with five repeats creates 600.

```bash
python3 scripts/build_run_matrix.py \
  --case-ids evals/smoke-case-ids.txt --repeats 3 \
  --out runs/smoke-plan.jsonl
```

1. Freeze `cases.jsonl`, `rubric.md`, metrics, and exclusions before collecting results.
2. Produce one JSONL file per condition using `output-schema.json`.
3. Create blinded pairs:

```bash
python3 scripts/make_blind_pairs.py \
  --left runs/baseline.jsonl --left-label baseline \
  --right runs/release.jsonl --right-label release \
  --pairs runs/blind-pairs.jsonl --key runs/blind-key.json \
  --seed 20260830
```

4. Have at least two blinded raters score every pair. Adjudicate large disagreements or add a third rater.
5. Aggregate with `scripts/aggregate_benchmark.py`.

## Honesty rule

Publish the suite version, exclusions, failed runs, raw blinded artifacts, and uncertainty intervals. A small sample, a static metric, or a strong anecdote is not proof of a baseline-versus-skill effect. A null or negative result is still useful: it identifies where the skill should not be used.
