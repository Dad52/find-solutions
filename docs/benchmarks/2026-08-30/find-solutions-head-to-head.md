# Find Solutions v0.1.0 — paired benchmark

This report compares ordinary Codex with an explicit `$find-solutions` invocation. It is a small, repeatable benchmark, not a claim about every kind of problem.

## Setup

- Worker: `gpt-5.6-terra`, `medium` reasoning.
- Blind judge: `gpt-5.6-sol`, `high` reasoning.
- Five fixed cases, three paired repeats each: 30 worker answers and 15 blind comparisons.
- Every worker had a new workspace. Only the candidate workspace contained Find Solutions; the judge received shuffled answers A/B and no condition label.
- The live-web case was excluded because availability and prices would make the result stale.

The judge applied the frozen Fast Frontier route gate: a counted route must respect every hard constraint, describe a concrete mechanism, name a feasible first action, expose a signal plus stop/rollback/fallback, and be decision-distinct from the other counted routes.

## Aggregate results

| Measure | Ordinary Codex | With Find Solutions |
| --- | ---: | ---: |
| Correct first-ranked route | 9 / 15 | **14 / 15** |
| Practical frontier routes, mean of up to five | 2.53 | 2.60 |
| Accepted decision-distinct routes, mean of up to five | **3.00** | 2.93 |
| Trap routes, total | 15 | **11** |
| Answers containing a hard-constraint breach | 6 / 15 | **4 / 15** |
| Top-three frontier success | 15 / 15 | 15 / 15 |
| Executable first step and stop/rollback | 15 / 15 | 15 / 15 |
| Blind preference | 6 wins, 2 ties | 7 wins, 2 ties |
| Median worker time | **21.9 s** | 22.8 s |
| Mean output tokens | **986** | 1,112 |

The useful change is ranking and constraint handling, not a larger option list. The cost in this run was about 4% more wall time and 13% more output tokens.

## Per-case results

| Case | Blind wins: ordinary / skill / tie | What changed |
| --- | ---: | --- |
| Accessible rainy-day plan | 2 / 1 / 0 | The skill picked the correct first itinerary in all three repeats, but both conditions sometimes offered an incomplete market-only route. |
| Duplicate payments | 2 / 1 / 0 | The skill picked the safer ambiguous-state route in all three repeats, while ordinary Codex offered more accepted alternatives overall. |
| Week-2 retention | 2 / 1 / 0 | The skill removed all judged constraint breaches and led more often with a causal discriminator; ordinary Codex still won two pairwise answers. |
| Strategy-game comeback | 0 / 3 / 0 | The skill avoided disguised catch-up grants and chose a cheaper, testable mechanism in every repeat. |
| Search migration holdout | 0 / 1 / 2 | Both began with safe shadow reads; neither consistently made the rollback drill and divergence budget concrete enough. |

## Three selected answer pairs

These are one measured Find Solutions win from each reader-facing domain. They are not the entire dataset; the tables above include the counterexamples.

### Life: a rainy Saturday with an injured knee

| Prompt constraint | Ordinary Codex | With Find Solutions |
| --- | --- | --- |
| No booking, rain-safe, food, 3,500-credit budget, no more than 35 minutes walking | Correctly chose the risograph demo plus food. Its alternate route did not verify the journey home. It also added a flea-market route without a complete food plan. | Chose the same risograph-plus-food route, then made the robotics route conditional on every transit leg, cumulative walking, seating, and the trip home. It removed the incomplete market route. |

### Business: weak week-2 retention without pretending correlation is causation

| Prompt constraint | Ordinary Codex | With Find Solutions |
| --- | --- | --- |
| One sprint; no redesign, discounts, notifications, or causal overclaim | Tested a narrower permission screen, but proposed a fallback that assumed a new manual/sample-data import path and asserted an unproven data-retention fact. | Tested just-in-time, purpose-specific permission requests; used import completion and useful-artifact export as guardrails; retained a small qualitative study as evidence gathering rather than proof. |

### Code: duplicate payment after an accepted-but-timed-out provider call

| Prompt constraint | Ordinary Codex | With Find Solutions |
| --- | --- | --- |
| Client retries stay on; no database change or provider replacement; Redis exists; deploy and reverse within a day | Used a Redis lease and short-lived outcome cache. The lease could expire before an ambiguous charge was reconciled, reopening the duplicate window. | Wrote a durable Redis `SENT → SUCCESS | AMBIGUOUS` state before the side effect; retries receive pending rather than another charge; the test forces accept-then-timeout and asserts one provider call. |

## Reproduce

The frozen plan and runner are in the release workspace under `work/find-solutions-head-to-head/`. Raw prompts and model outputs are deliberately not packaged: they are transient evidence and may contain user-like scenarios. The plan records the models, efforts, case IDs, condition isolation, and metric definitions needed to repeat the comparison.
