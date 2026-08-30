#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = {
    "baseline": {
        "setup": "Run with find-solutions and comparison skills absent/disabled.",
        "prefix": "",
    },
    "release": {
        "setup": "Install the pinned v0.1.0 release as the explicit find-solutions skill.",
        "prefix": "$find-solutions ",
    },
    "current": {
        "setup": "Install the pinned current find-solutions skill under comparison.",
        "prefix": "$find-solutions ",
    },
    "candidate": {
        "setup": "Install the candidate find-solutions skill under comparison.",
        "prefix": "$find-solutions ",
    },
    "adhd": {
        "setup": "Install and pin UditAkhourii/adhd; use only on the declared overlap subset.",
        "prefix": "/adhd ",
    },
}


def load_cases(path: Path, selected: set[str] | None) -> list[dict]:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if selected is not None:
        records = [r for r in records if r["id"] in selected]
        missing = selected - {r["id"] for r in records}
        if missing:
            raise ValueError(f"unknown case IDs: {sorted(missing)}")
    return records


def main() -> int:
    p = argparse.ArgumentParser(description="Create a randomized, host-neutral A/B/C run plan")
    p.add_argument("--cases", type=Path, default=ROOT / "evals/cases.jsonl")
    p.add_argument("--case-ids", type=Path, help="Optional newline-separated subset")
    p.add_argument("--conditions", nargs="+", choices=sorted(CONDITIONS), default=["baseline", "release"])
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--seed", type=int, default=20260830)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.repeats < 1:
        raise ValueError("repeats must be >= 1")

    selected = None
    if args.case_ids:
        selected = {line.strip() for line in args.case_ids.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
    cases = load_cases(args.cases, selected)
    rows = []
    for case in cases:
        for repeat in range(1, args.repeats + 1):
            sample_id = f"r{repeat:02d}"
            for condition in args.conditions:
                task = case["prompt"]
                spec = CONDITIONS[condition]
                run_prompt = f"{spec['prefix']}{task}"
                rows.append({
                    "case_id": case["id"],
                    "sample_id": sample_id,
                    "condition": condition,
                    "mode": case.get("mode"),
                    "domain": case.get("domain"),
                    "task_prompt": task,
                    "run_prompt": run_prompt,
                    "condition_setup": spec["setup"],
                    "hard_constraints": case.get("hard_constraints", []),
                    "requires_web": bool(case.get("requires_web", False)),
                })
    random.Random(args.seed).shuffle(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for order, row in enumerate(rows, 1):
            row["randomized_order"] = order
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} run slots for {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
