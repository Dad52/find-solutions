# Development audit: early draft to public release candidate

## What the early draft got right

- It separates an option, a mechanism, and an executable route instead of counting wording variants.
- It searches reuse, buying, delegation, subtraction, no-action, constraint bypass, diagnosis, and transfer.
- It treats community material as a hypothesis lead rather than proof of current availability.
- It retains competing causal hypotheses and discriminators when the cause is uncertain.
- It requires executable artifacts, tests, fallbacks, stop rules, and explicit evidence gaps.

Those are the core assets preserved in the public release candidate.

## Structural changes before release

| Earlier risk | Release-candidate response |
| --- | --- |
| A narrow task could expand into a high-latency option dump. | Start with a small rescue route and stop when another search pass cannot change the decision. |
| Research happened before source-free mechanism expansion. | Generate distinct mechanisms first; retrieve only to resolve decision-relevant uncertainty. |
| Host- and model-specific instructions reduced portability. | Route by available capability and degrade gracefully. |
| Large references could be read without a task-specific reason. | Load only the selected domain and evidence/output guidance. |
| Broken links, manifests, and evaluation fixtures could pass unnoticed. | Include standard-library validation, tests, blind pairing, aggregation, and CI. |

## Claims deliberately not made

The public v0.1.0 release does not claim that the workflow is better, faster, or cheaper in live model runs. Its static checks and evaluation fixtures make that question testable; they do not answer it. See [evals/README.md](../evals/README.md) for the preregistered baseline-versus-release protocol.
