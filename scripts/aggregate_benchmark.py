#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def cluster_bootstrap_ci(rows: list[tuple[str, float]], seed: int = 20260819, draws: int = 5000) -> tuple[float, float] | None:
    """Bootstrap case clusters so repeats and raters do not create fake sample size."""
    if not rows:
        return None
    by_case: dict[str, list[float]] = defaultdict(list)
    for case_id, value in rows:
        by_case[case_id].append(value)
    cases = sorted(by_case)
    case_means = {case: statistics.fmean(by_case[case]) for case in cases}
    if len(cases) == 1:
        value = case_means[cases[0]]
        return value, value
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(draws):
        picked = [cases[rng.randrange(len(cases))] for _ in cases]
        samples.append(statistics.fmean(case_means[c] for c in picked))
    samples.sort()
    return samples[int(0.025 * draws)], samples[int(0.975 * draws) - 1]


def percentile(values: list[float], fraction: float) -> float:
    """Nearest-rank percentile for compact benchmark summaries."""
    if not values:
        raise ValueError("percentile requires at least one value")
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(fraction * len(ordered) + 0.999999) - 1))
    return ordered[index]


def main() -> int:
    p = argparse.ArgumentParser(description="Unblind ratings and aggregate paired, case-clustered benchmark results")
    p.add_argument("--pairs", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--ratings", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    pairs = {r["pair_id"]: r for r in jsonl(args.pairs)}
    key_obj = json.loads(args.key.read_text(encoding="utf-8"))
    keys = {r["pair_id"]: r for r in key_obj["pairs"]}
    ratings = jsonl(args.ratings)

    ratings_by_pair: dict[str, list[dict]] = defaultdict(list)
    for rating in ratings:
        pair_id = rating["pair_id"]
        if pair_id not in pairs or pair_id not in keys:
            raise ValueError(f"rating references unknown pair: {pair_id}")
        ratings_by_pair[pair_id].append(rating)

    # Collapse raters to one observation per output pair before inferential summaries.
    condition_scores: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    paired_diffs: dict[tuple[str, str, str], list[tuple[str, float]]] = defaultdict(list)
    preference = Counter()
    critical_pairs = Counter()

    for pair_id, pair_ratings in sorted(ratings_by_pair.items()):
        mapping = keys[pair_id]
        pair = pairs[pair_id]
        side_for_condition = {mapping["A"]: "A", mapping["B"]: "B"}
        conditions = sorted(side_for_condition)
        if len(conditions) != 2:
            raise ValueError(f"pair {pair_id} does not contain two distinct conditions")

        side_dimension_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        pref_votes = Counter()
        for rating in pair_ratings:
            for side in ("A", "B"):
                for dimension, value in rating.get("scores", {}).get(side, {}).items():
                    side_dimension_values[side][dimension].append(float(value))
                if rating.get("critical_failure", {}).get(side):
                    critical_pairs[mapping[side]] += 1
            pref = rating.get("preference", "tie")
            pref_votes[mapping[pref] if pref in ("A", "B") else "tie"] += 1

        # Majority preference per pair; disagreement becomes tie.
        ranked_votes = pref_votes.most_common()
        if not ranked_votes or (len(ranked_votes) > 1 and ranked_votes[0][1] == ranked_votes[1][1]):
            preference["tie"] += 1
        else:
            preference[ranked_votes[0][0]] += 1

        pair_means: dict[str, dict[str, float]] = defaultdict(dict)
        for side in ("A", "B"):
            condition = mapping[side]
            for dimension, values in side_dimension_values[side].items():
                mean_value = statistics.fmean(values)
                pair_means[condition][dimension] = mean_value
                condition_scores[condition][dimension].append(mean_value)

        left, right = conditions
        common_dims = set(pair_means[left]) & set(pair_means[right])
        for dim in common_dims:
            paired_diffs[(left, right, dim)].append((pair["case_id"], pair_means[right][dim] - pair_means[left][dim]))

    lines = [
        "# Benchmark report",
        "",
        f"Rated output pairs: {len(ratings_by_pair)}; raw rating records: {len(ratings)}; generated pairs: {len(pairs)}",
        "",
        "Rater scores are averaged within each output pair. Confidence intervals resample case clusters, not individual repeats or raters.",
        "",
        "## Pair-level blind preference",
        "",
    ]
    total = sum(preference.values()) or 1
    for label, count in sorted(preference.items()):
        lines.append(f"- {label}: {count:g} ({100*count/total:.1f}%)")

    lines += ["", "## Mean pair-level rubric scores", "", "| condition | dimension | mean | pairs |", "|---|---|---:|---:|"]
    for condition in sorted(condition_scores):
        for dim in sorted(condition_scores[condition]):
            vals = condition_scores[condition][dim]
            lines.append(f"| {condition} | {dim} | {statistics.fmean(vals):.3f} | {len(vals)} |")

    lines += [
        "",
        "## Paired differences with case-clustered bootstrap",
        "",
        "Positive means the alphabetically second condition scored higher.",
        "",
        "| contrast | dimension | mean difference | case-clustered 95% CI | pairs | cases |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for (left, right, dim), rows in sorted(paired_diffs.items()):
        values = [value for _, value in rows]
        ci = cluster_bootstrap_ci(rows)
        ci_text = "n/a" if ci is None else f"[{ci[0]:.3f}, {ci[1]:.3f}]"
        lines.append(
            f"| {right} − {left} | {dim} | {statistics.fmean(values):.3f} | {ci_text} | {len(rows)} | {len({case for case, _ in rows})} |"
        )

    lines += ["", "## Critical-failure ratings", ""]
    if critical_pairs:
        for condition, count in sorted(critical_pairs.items()):
            lines.append(f"- {condition}: {count}")
    else:
        lines.append("- none recorded")

    metric_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for pair_id, pair in pairs.items():
        mapping = keys[pair_id]
        for side in ("A", "B"):
            condition = mapping[side]
            for metric in (
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "reasoning_tokens",
                "total_tokens",
                "wall_time_s",
                "tool_calls",
            ):
                value = pair.get(side, {}).get(metric)
                if isinstance(value, (int, float)):
                    metric_values[condition][metric].append(float(value))
    lines += ["", "## Efficiency", "", "| condition | metric | median | p90 | mean | n outputs |", "|---|---|---:|---:|---:|---:|"]
    for condition in sorted(metric_values):
        for metric, vals in sorted(metric_values[condition].items()):
            lines.append(
                f"| {condition} | {metric} | {statistics.median(vals):.3f} | "
                f"{percentile(vals, 0.9):.3f} | {statistics.fmean(vals):.3f} | {len(vals)} |"
            )

    lines += [
        "",
        "## Interpretation guardrail",
        "",
        "This report is descriptive unless conditions used identical runtime settings, randomized execution order, disclosed failures/exclusions, and preregistered metrics. Multiple outputs from one case improve reliability but do not create independent problem domains.",
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
