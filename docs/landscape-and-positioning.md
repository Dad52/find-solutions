# Landscape and positioning

Checked: 2026-08-19. This is a sampled public-repository review, not an exhaustive census.

## Closest categories

| Project / skill | Strong at | Missing relative to find-solutions |
|---|---|---|
| UditAkhourii/adhd | isolated parallel divergence, generator/critic separation, clustering, trap pruning, and public ideation evals | optimizes novelty/breadth for open-ended ideation; not a current-fact research, procurement, evidence-calibration, or shortest-route decision workflow; default architecture is materially more expensive |
| obra/superpowers `brainstorming` | turning software ideas into approved designs; scope classification and hard design gates | not an evidence-aware route portfolio; mostly 2–3 design approaches; not a general rescue/ranking workflow |
| Anthropic `product-brainstorming` | problem exploration, divergence, assumption testing, product frameworks | intentionally conversational and not a deliverable; no current-fact verification or executable ranked portfolio |
| K-Dense `scientific-brainstorming` | evidence-aware scientific ideation, adversarial review, explicit assumptions | scientific domain; does not optimize a shortest cross-domain execution route |
| `rtovardev/muse` | cross-domain ideation from personal/project memory, web signals, confidence and falsifiers | optimizes recurring idea discovery and taste learning; writes a dream ledger rather than ranking routes around one concrete blocker |
| RCA / debugging skills | causal hypotheses, diagnosis, tests, root-cause isolation | usually assume the answer is a fix inside the current system; weak on buy/delegate/remove/change-boundary routes |
| Deep-research skills | source collection, synthesis, citations | may research the current framing deeply without first expanding mechanism families or producing a reversible action portfolio |
| Decision frameworks | criteria, trade-offs, scoring | often rank supplied options rather than discover routes, verify availability, and recover from failed attempts |

The closest direct substitute is ADHD: both try to escape local search failure by forcing decision-distinct branches. It should be treated as the primary comparator on open-ended technical and product cases, not waved away as a generic brainstorming skill. The sampled search still found no exact public duplicate of: **explicit rescue trigger + source-free mechanism expansion + gap-targeted current-fact research + evidence calibration + executable route ranking + fallback/stop rules across technical, market, operations, procurement, and general decisions**. That is a defensible differentiation claim only within the sampled repositories.

## Is it needed?

There is credible ecosystem demand for reusable agent workflows: agent-skill and plugin repositories have large active communities, and brainstorming/research skills recur across major collections. That supports the category, not this exact product.

The sharper demand hypothesis is:

> After an agent has tried the obvious route and starts repeating local fixes, a user wants one explicit command that expands the solution boundary and returns a credible next move without paying for a full deep-research report.

That is stronger than positioning it as “a skill that generates many ideas.” Quantity is easy to imitate and can reduce trust. The wedge is **recovery from local search failure**.

## Target users

- engineers whose agent is repeating fixes inside one architecture;
- founders and product managers who need manual/reuse/buy/partner tests before building;
- operations users facing access, booking, queue, handoff, or ownership constraints;
- researchers who need a bounded transfer or a disconfirming experiment rather than another literature summary.

## Risks

1. **Too broad to trigger mentally.** Solve with an explicit rescue phrase and before/after examples.
2. **Output overwhelms the decision.** Rescue mode must remain the default; 20–30 routes belong only in deep mode.
3. **“More ideas” becomes cosmetic variants.** Benchmark decision-distinct mechanisms and usable routes, not counts.
4. **Evidence ceremony consumes the gain.** Verify claims that can change rank, not every low-ranked candidate.
5. **Host-specific orchestration breaks.** Keep the core capability-based and test Codex/Claude separately.
6. **One impressive anecdote is mistaken for proof.** Publish paired repeated results and raw blinded artifacts.
7. **A breadth win is claimed without beating the strongest comparator.** Run the optional ADHD arm on the ideation subset and report quality together with token/time cost.

## Minimum viable launch

1. Publish v0.1.0 with redacted, factual examples only; do not present before/after cases as effectiveness proof before the paired evaluation is complete.
2. Recruit 10–20 users who already have a stuck task; do not ask them to invent toy prompts.
3. Record whether the skill changed the chosen action, not just whether the answer looked better.
4. Run the preregistered A/B/C suite and publish failures as well as wins.
5. Use GitHub issue labels: `duplicate-routes`, `constraint-violation`, `unsupported-claim`, `bad-rank`, `too-slow`, `missing-route`, `great-rescue`.

## Product promise

Recommended one-line promise:

> **When your agent is stuck, find the shortest credible route around the blocker.**

Recommended repository subtitle:

> Evidence-aware solution search for agents: distinct mechanisms, executable routes, verification, tests, and fallbacks.


## Direct comparison hypothesis: find-solutions vs ADHD

| Dimension | ADHD advantage hypothesis | find-solutions advantage hypothesis |
|---|---|---|
| divergent novelty | stronger due to mechanically isolated cognitive frames | adequate breadth, but optimized for decision relevance rather than novelty |
| trap discovery | strong explicit critic/pruning stage | hard-constraint gates, failed-attempt exclusion, disconfirmers, and stop/rollback checks |
| current facts | not the primary product | gap-targeted web verification, freshness, availability status, and claim calibration |
| route breadth | strongest inside ideation/design space | includes access, self-service, reuse, buy, hire, delegate, remove, no-action, constraint change, diagnosis, automation, and build |
| output cost | multi-call architecture is intentionally expensive | rescue mode should be substantially cheaper; this remains to be measured |
| local/procurement tasks | outside the main fit | first-class domain with booking channel, all-in cost, verification, and fallback |
| decision handoff | deepened concepts and first steps | owner, 1–3 actions, artifact/signal, falsifier, stop/rollback, fallback, and copy-ready handoff |

Do not claim that either system wins overall. Compare only where scopes overlap, publish per-domain results, and preserve a trade-off conclusion when ADHD buys more novelty with more calls while find-solutions buys more verification or efficiency.

## Public sources sampled

- [ADHD repository](https://github.com/UditAkhourii/adhd)
- [ADHD preprint and eval summary](https://adhdstack.github.io/)
- [obra/superpowers brainstorming skill](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md)
- [Anthropic product-brainstorming skill](https://github.com/anthropics/knowledge-work-plugins/blob/main/product-management/skills/product-brainstorming/SKILL.md)
- [Muse repository](https://github.com/rtovardev/muse)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI plugin examples](https://github.com/openai/plugins)
