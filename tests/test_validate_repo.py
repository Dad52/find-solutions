from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ValidateRepoTest(unittest.TestCase):
    def test_validator_passes(self):
        module = load_module("validate_repo", ROOT / "scripts/validate_repo.py")
        self.assertEqual([], module.validate())

    def test_case_count_and_ids(self):
        records = [json.loads(line) for line in (ROOT / "evals/cases.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(records), 60)
        self.assertEqual(len(records), len({r["id"] for r in records}))

    def test_explicit_only_policy(self):
        text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", text)

    def test_fast_frontier_cases_and_gold_match(self):
        fast = ROOT / "evals/fast-frontier"
        cases = [json.loads(line) for line in (fast / "cases.jsonl").read_text(encoding="utf-8").splitlines() if line]
        gold = [json.loads(line) for line in (fast / "gold.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertEqual(8, len(cases))
        self.assertEqual({r["id"] for r in cases}, {r["id"] for r in gold})
        headline = {
            line for line in (fast / "headline-case-ids.txt").read_text(encoding="utf-8").splitlines()
            if line and not line.startswith("#")
        }
        holdout = {
            line for line in (fast / "holdout-case-ids.txt").read_text(encoding="utf-8").splitlines()
            if line and not line.startswith("#")
        }
        self.assertEqual(6, len(headline))
        self.assertEqual(2, len(holdout))
        self.assertFalse(headline & holdout)
        self.assertEqual({r["id"] for r in cases}, headline | holdout)
        self.assertEqual({False}, {r["requires_web"] for r in cases if r["id"] in headline})

    def test_solution_operators_are_reachable_and_bounded(self):
        core = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        research = (ROOT / "references/research-lanes.md").read_text(encoding="utf-8")
        operators = (ROOT / "references/solution-operators.md").read_text(encoding="utf-8")
        self.assertTrue(
            "references/solution-operators.md" in core or "solution-operators.md" in research,
            "solution operators must be reachable from the runtime disclosure graph",
        )
        for required in [
            "Move the intervention",
            "Change the causal lever",
            "Invert a credible failure chain",
            "Test an extreme constraint",
            "Replace expensive prevention",
            "Search another domain",
        ]:
            self.assertIn(required, operators)
        self.assertIn("Stop rather than fill", operators)
        self.assertIn(
            "not as mandatory idea categories",
            (ROOT / "references/research-lanes.md").read_text(encoding="utf-8"),
        )

    def test_eval_artifacts_do_not_ship(self):
        self.assertIn(".skill-forge/", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        package_script = (ROOT / "scripts/package_release.py").read_text(encoding="utf-8")
        self.assertIn('".skill-forge"', package_script)


if __name__ == "__main__":
    unittest.main()
