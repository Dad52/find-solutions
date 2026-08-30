#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter has no closing delimiter")
    raw = text[4:end]
    body = text[end + 5 :]
    values: dict[str, str] = {}
    current = None
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            raise ValueError(f"Malformed top-level frontmatter line: {line}")
        key, value = line.split(":", 1)
        current = key.strip()
        values[current] = value.strip().strip('"\'')
    return values, body


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILL.exists():
        return [f"missing {SKILL.relative_to(ROOT)}"]

    text = SKILL.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = fm.get("name", "")
    description = fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(errors, "frontmatter name must be lowercase kebab-case")
    if name != SKILL.parent.name:
        fail(errors, "frontmatter name must match skill directory")
    if not description or len(description) > 1024:
        fail(errors, "description must be 1..1024 characters")
    if len(text.splitlines()) > 500:
        fail(errors, "SKILL.md exceeds 500 lines")
    if "Use only when explicitly invoked as $find-solutions" not in description:
        fail(errors, "description must state the explicit-only invocation boundary")

    # Relative Markdown links from SKILL.md.
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (SKILL.parent / target).resolve()
        try:
            resolved.relative_to(SKILL.parent.resolve())
        except ValueError:
            fail(errors, f"link escapes skill root: {target}")
            continue
        if not resolved.exists():
            fail(errors, f"broken SKILL.md link: {target}")

    # Host-neutral core: reject named model coupling inside the distributed skill.
    named_model = re.compile(r"\b(?:gpt-[0-9]|claude-(?:opus|sonnet|haiku)|gemini-[0-9])", re.I)
    operational_docs = [SKILL, *(ROOT / "references").rglob("*.md")]
    for path in operational_docs:
        if named_model.search(path.read_text(encoding="utf-8")):
            fail(errors, f"hard-coded model name in distributed skill: {path.relative_to(ROOT)}")

    required_json = [
        ROOT / ".agents/plugins/marketplace.json",
        ROOT / ".claude-plugin/marketplace.json",
        ROOT / ".codex-plugin/plugin.json",
        ROOT / ".claude-plugin/plugin.json",
        ROOT / "evals/output-schema.json",
        ROOT / "evals/fast-frontier/rating-record.example.json",
    ]
    for path in required_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            fail(errors, f"missing JSON: {path.relative_to(ROOT)}")
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    for rel, minimum in [("evals/cases.jsonl", 50), ("evals/trigger-cases.jsonl", 20)]:
        path = ROOT / rel
        ids: set[str] = set()
        count = 0
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            fail(errors, f"missing {rel}")
            continue
        for n, line in enumerate(lines, 1):
            if not line.strip():
                continue
            count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(errors, f"{rel}:{n}: invalid JSON: {exc}")
                continue
            rid = record.get("id")
            if not rid:
                fail(errors, f"{rel}:{n}: missing id")
            elif rid in ids:
                fail(errors, f"{rel}:{n}: duplicate id {rid}")
            ids.add(rid)
        if count < minimum:
            fail(errors, f"{rel} has {count} cases; expected at least {minimum}")

    fast_dir = ROOT / "evals/fast-frontier"

    def load_jsonl(rel: str) -> list[dict]:
        path = ROOT / rel
        records: list[dict] = []
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            fail(errors, f"missing {rel}")
            return records
        for n, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(errors, f"{rel}:{n}: invalid JSON: {exc}")
                continue
            records.append(record)
        return records

    fast_cases = load_jsonl("evals/fast-frontier/cases.jsonl")
    fast_gold = load_jsonl("evals/fast-frontier/gold.jsonl")
    case_ids = [r.get("id") for r in fast_cases]
    gold_ids = [r.get("id") for r in fast_gold]
    if len(fast_cases) != 8:
        fail(errors, f"fast-frontier must contain exactly 8 cases; found {len(fast_cases)}")
    if len(case_ids) != len(set(case_ids)):
        fail(errors, "fast-frontier cases contain duplicate IDs")
    if len(gold_ids) != len(set(gold_ids)):
        fail(errors, "fast-frontier gold contains duplicate IDs")
    if set(case_ids) != set(gold_ids):
        fail(errors, "fast-frontier case IDs and gold IDs must match exactly")
    for record in fast_cases:
        for key in ("id", "prompt", "hard_constraints", "primary_metrics"):
            if not record.get(key):
                fail(errors, f"fast-frontier case {record.get('id', '<unknown>')} missing {key}")
    for record in fast_gold:
        for key in ("id", "frontier_families", "conditional_winners", "traps", "objective_checks"):
            if not record.get(key):
                fail(errors, f"fast-frontier gold {record.get('id', '<unknown>')} missing {key}")

    def load_id_file(name: str) -> set[str]:
        path = fast_dir / name
        try:
            return {
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.startswith("#")
            }
        except FileNotFoundError:
            fail(errors, f"missing evals/fast-frontier/{name}")
            return set()

    headline_ids = load_id_file("headline-case-ids.txt")
    holdout_ids = load_id_file("holdout-case-ids.txt")
    if len(headline_ids) != 6 or len(holdout_ids) != 2:
        fail(errors, "fast-frontier requires 6 headline IDs and 2 holdout IDs")
    if headline_ids & holdout_ids:
        fail(errors, "fast-frontier headline and holdout IDs overlap")
    if headline_ids | holdout_ids != set(case_ids):
        fail(errors, "fast-frontier ID lists must partition all cases")

    openai_meta = ROOT / "agents/openai.yaml"
    meta_text = openai_meta.read_text(encoding="utf-8") if openai_meta.exists() else ""
    if "allow_implicit_invocation: false" not in meta_text:
        fail(errors, "Codex explicit-only policy is missing")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: repository structure, skill metadata, links, manifests, and eval IDs are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
