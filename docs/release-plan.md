# Open-source release plan

## Before publishing v0.1.0

1. Confirm the public identity `Dad52`, the repository `Dad52/find-solutions`, and the MIT copyright line.
2. Run `make check` and install the release into a clean Codex project with `npx skills add`.
3. Confirm that generated data, local run artifacts, and private traces remain excluded by `.gitignore` and the package script.
4. Publish no effectiveness, token, or competitor claim until it has a matching blinded run artifact.
5. Add a real, redacted example only when its facts, constraints, and outcome can be checked.
6. Tag `v0.1.0`.

## First public month

- Week 1: installation and trigger reliability; fix portability before expanding the workflow.
- Week 2: collect real stuck tasks and classify failure modes.
- Week 3: freeze the benchmark rubric and run the baseline-versus-release smoke suite.
- Week 4: publish a benchmark report with raw run manifests, token/time distributions, paired confidence intervals, and known regressions.

## Promotion gate to beta

Promote only when:

- installation succeeds on at least two supported hosts;
- no critical constraint or safety failure appears in the adversarial suite;
- the baseline-versus-release evaluation shows a positive paired effect on the preregistered primary metric across at least three domains;
- any cost increase is explicit and accepted, or quality is non-inferior at a lower measured cost;
- at least five real users report that the output changed their next action.
