# Contributing

Contributions should improve decision quality, portability, or measured efficiency rather than add more ceremony.

## Best issue format

Include:

1. the exact invocation and host/version;
2. outcome, hard constraints, and already-tried routes;
3. selected mode and available capabilities (web, workers, files);
4. full output or a redacted reproducible excerpt;
5. the failure: duplicate routes, violated constraint, unsupported claim, bad ranking, drift, excessive tokens, or missing fallback;
6. the smallest change that would have altered your decision.

Never include secrets, private customer data, or credentials.

## Pull requests

- Keep `SKILL.md` focused and route domain detail into one-level references.
- Do not add a named model or host-specific worker API to the core workflow.
- Add or update an eval case for every behavioral change.
- Run `python3 scripts/validate_repo.py` and `python3 -m unittest discover -s tests -v`.
- Do not claim an improvement from one example. Attach the benchmark run manifest and paired results.

## Evaluation changes

Changes to the primary metric, exclusion rules, or rubric require a versioned methodology note before seeing new results. This prevents moving the goalposts after a preferred result appears.
