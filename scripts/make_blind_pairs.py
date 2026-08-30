#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def load(path: Path) -> dict[tuple[str, str], dict]:
    records: dict[tuple[str, str], dict] = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rec = json.loads(line)
        key = (rec["case_id"], rec["sample_id"])
        if key in records:
            raise ValueError(f"duplicate {key} in {path}:{n}")
        records[key] = rec
    return records


def main() -> int:
    p = argparse.ArgumentParser(description="Create randomized A/B output pairs and a private unblinding key")
    p.add_argument("--left", type=Path, required=True)
    p.add_argument("--left-label", required=True)
    p.add_argument("--right", type=Path, required=True)
    p.add_argument("--right-label", required=True)
    p.add_argument("--pairs", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--seed", type=int, default=20260819)
    args = p.parse_args()

    left, right = load(args.left), load(args.right)
    common = sorted(left.keys() & right.keys())
    missing_left = sorted(right.keys() - left.keys())
    missing_right = sorted(left.keys() - right.keys())
    if missing_left or missing_right:
        raise ValueError(f"unmatched records: missing-left={len(missing_left)}, missing-right={len(missing_right)}")

    rng = random.Random(args.seed)
    pairs, key_records = [], []
    for case_id, sample_id in common:
        l, r = left[(case_id, sample_id)], right[(case_id, sample_id)]
        swap = bool(rng.getrandbits(1))
        a, b = (r, l) if swap else (l, r)
        pair_id = f"{case_id}::{sample_id}"
        def public_output(record: dict) -> dict:
            return {
                "output": record.get("output", ""),
                "input_tokens": record.get("input_tokens"),
                "cached_input_tokens": record.get("cached_input_tokens"),
                "output_tokens": record.get("output_tokens"),
                "reasoning_tokens": record.get("reasoning_tokens"),
                "total_tokens": record.get("total_tokens"),
                "wall_time_s": record.get("wall_time_s"),
                "tool_calls": record.get("tool_calls"),
                "error": record.get("error"),
            }

        pairs.append({
            "pair_id": pair_id,
            "case_id": case_id,
            "sample_id": sample_id,
            "A": public_output(a),
            "B": public_output(b),
        })
        key_records.append({
            "pair_id": pair_id,
            "A": args.right_label if swap else args.left_label,
            "B": args.left_label if swap else args.right_label,
        })

    args.pairs.parent.mkdir(parents=True, exist_ok=True)
    args.key.parent.mkdir(parents=True, exist_ok=True)
    with args.pairs.open("w", encoding="utf-8") as f:
        for rec in pairs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    args.key.write_text(json.dumps({"seed": args.seed, "pairs": key_records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(pairs)} blinded pairs and private key")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
