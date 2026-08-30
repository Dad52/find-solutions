#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path


def sentence_duplicate_ratio(text: str) -> float:
    sentences = [re.sub(r"\s+", " ", s.strip().lower()) for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.strip()) >= 25]
    if not sentences:
        return 0.0
    return 1.0 - len(set(sentences)) / len(sentences)


def main() -> int:
    p = argparse.ArgumentParser(description="Compute cheap text diagnostics; not a quality score")
    p.add_argument("inputs", type=Path, nargs="+")
    args = p.parse_args()
    rows = []
    for path in args.inputs:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            text = rec.get("output", "")
            rows.append({
                "file": str(path),
                "condition": rec.get("condition"),
                "case_id": rec.get("case_id"),
                "words": len(re.findall(r"\S+", text)),
                "chars": len(text),
                "duplicate_sentence_ratio": sentence_duplicate_ratio(text),
                "reported_output_tokens": rec.get("output_tokens"),
                "wall_time_s": rec.get("wall_time_s"),
            })
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
