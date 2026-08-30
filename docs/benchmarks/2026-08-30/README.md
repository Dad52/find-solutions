# Release benchmark — 2026-08-30

This is a small release check for Find Solutions v0.1.0. It compares ordinary
Codex with the same Codex run after an explicit `$find-solutions` invocation.
The purpose is to record what was actually checked, not to turn a passing JSON
shape into a claim about better judgment.

## Setup

- Worker: Codex `gpt-5.6-terra`, `xhigh` reasoning.
- Three synthetic but practical cases: a rain- and mobility-constrained day,
  a privacy-product retention problem, and duplicate payments after an
  ambiguous timeout.
- Three isolated repetitions per case and condition: 18 runs in total.
- Every run had a fresh workspace. The prompt, model, effort, time limit, and
  requested output shape were the same; only the skill invocation changed.
- No model judge was used. The published checks are deterministic.

## Measured result

| Measure | Codex without the skill | Codex with Find Solutions |
| --- | ---: | ---: |
| Runs completing the harness | 9 / 9 | 9 / 9 |
| Valid response object with at least one route | 9 / 9 | 9 / 9 |
| Every returned route has action, signal, stop/rollback, and fallback fields | 9 / 9 | 9 / 9 |
| No byte-identical `mechanism` label inside one response | 9 / 9 | 9 / 9 |
| Median output tokens | 1,527 | 1,570 (+2.8%) |
| Median wall time | 23.9 s | 25.7 s (+7.5%) |
| P90 wall time | 53.5 s | 66.4 s |

The deterministic checks did not distinguish the two conditions. In this
small run, Find Solutions also used a little more output and time. So this
report does **not** claim a measured quality lift, token saving, or general
advantage over ordinary Codex.

It does show that the release candidate kept the response contract on three
different kinds of blocked work. Whether one route is genuinely more useful
than another needs a blinded semantic judge or a real-world outcome study;
neither is represented by these numbers.

## Inspect or rerun

- [evaluation-plan.json](evaluation-plan.json) records the conditions,
  assertions, and limits.
- [cases.jsonl](cases.jsonl) contains the three public prompts.
- [results.json](results.json) preserves every sanitized run record,
  assertion, token count, timing value, and SHA-256 of the final response.

The answers themselves were kept out of the release artifact so the benchmark
does not publish machine-specific temporary paths. The prompts are synthetic;
there is no user data in this evidence set.
