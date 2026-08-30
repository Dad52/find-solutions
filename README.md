# Find Solutions

[Русский](README.ru.md)

> Find a workable solution when the obvious options have already failed.

Find Solutions is a manual, read-only skill for a task that has genuinely got
stuck. It keeps the outcome and hard constraints in view, rejects a renamed
version of an attempt that already failed, and returns a concrete next move
with a signal, a stop rule, and a fallback.

Use it when more ideas would just create a longer list. Don't use it for a
routine task with an obvious answer or to make an external change: it can
research and recommend, but it will not deploy, post, book, buy, or contact
anyone.

## What the benchmark found

In 15 paired, blind-judged runs, Find Solutions chose the correct first route
**14 times**; ordinary Codex did so **9 times**. It also produced fewer trap
routes and fewer answers with a hard-constraint breach. Both conditions still
found at least one viable route in every run.

| Measure | Ordinary Codex | With Find Solutions |
| --- | ---: | ---: |
| Correct first-ranked route | 9 / 15 | **14 / 15** |
| Trap routes | 15 | **11** |
| Answers with a hard-constraint breach | 6 / 15 | **4 / 15** |
| Practical routes, mean of up to five | 2.53 | 2.60 |
| Median response time | **21.9 s** | 22.8 s |
| Mean output tokens | **986** | 1,112 |

The skill improves the first decision, not speed or brevity. [The full report](docs/benchmarks/2026-08-30/find-solutions-head-to-head.md) includes the cases, rubric, counterexamples, and three selected answer pairs.

## What it looks like in practice

| Situation | Without the skill | With Find Solutions |
| --- | --- | --- |
| A rainy Saturday with an injured knee | The fallback missed a required trip-home check and added an incomplete market-only option. | The alternate itinerary is conditional on every travel leg, seating, total walking, and the way home. |
| Week-2 retention with misleading correlations | A reasonable experiment, but the fallback assumed an unsupplied feature and made an unsupported privacy claim. | A small permission experiment, downstream guardrails, and a separate evidence-gathering route without claiming causation. |
| Duplicate payment after a timeout | A short Redis lease could expire before the provider outcome is known. | A durable `SENT → SUCCESS | AMBIGUOUS` state blocks another charge until reconciliation. |

## Install

```bash
npx skills add Dad52/find-solutions --skill find-solutions --agent codex
```

## Use it

```text
$find-solutions Our Android CI still takes nearly an hour. We have already tuned caching, parallelized jobs, and moved to bigger runners. What can we try this week without rebuilding the pipeline?
```

It helps to give the outcome, the attempts that failed, hard constraints, the
deadline, access you already have, and what would count as a useful signal.
If one missing fact would change the available solution families, it asks once;
otherwise it states the assumption and gets on with the work.

## License

[MIT](LICENSE).
