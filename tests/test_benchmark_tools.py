from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BenchmarkToolsTest(unittest.TestCase):
    def test_blind_and_aggregate(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            left, right = d / "left.jsonl", d / "right.jsonl"
            left.write_text(json.dumps({"case_id":"c1","sample_id":"s1","condition":"baseline","output":"left","input_tokens":200,"output_tokens":100,"total_tokens":300,"tool_calls":2,"wall_time_s":1.0}) + "\n", encoding="utf-8")
            right.write_text(json.dumps({"case_id":"c1","sample_id":"s1","condition":"release","output":"right","input_tokens":180,"output_tokens":80,"total_tokens":260,"tool_calls":1,"wall_time_s":0.8}) + "\n", encoding="utf-8")
            pairs, key = d / "pairs.jsonl", d / "key.json"
            subprocess.run([
                "python3", str(ROOT / "scripts/make_blind_pairs.py"),
                "--left", str(left), "--left-label", "baseline",
                "--right", str(right), "--right-label", "release",
                "--pairs", str(pairs), "--key", str(key), "--seed", "1"
            ], check=True, capture_output=True, text=True)
            self.assertTrue(pairs.exists())
            mapping = json.loads(key.read_text(encoding="utf-8"))["pairs"][0]
            better_side = "A" if mapping["A"] == "release" else "B"
            worse_side = "B" if better_side == "A" else "A"
            rating = {
                "pair_id":"c1::s1", "rater":"r1", "preference":better_side,
                "critical_failure":{"A":False,"B":False},
                "scores":{
                    better_side:{"usable_route_at_5":4,"recovery_success_at_3":1},
                    worse_side:{"usable_route_at_5":2,"recovery_success_at_3":0}
                }
            }
            ratings = d / "ratings.jsonl"
            ratings.write_text(json.dumps(rating) + "\n", encoding="utf-8")
            report = d / "report.md"
            subprocess.run([
                "python3", str(ROOT / "scripts/aggregate_benchmark.py"),
                "--pairs", str(pairs), "--key", str(key),
                "--ratings", str(ratings), "--out", str(report)
            ], check=True, capture_output=True, text=True)
            text = report.read_text(encoding="utf-8")
            self.assertIn("release", text)
            self.assertIn("output_tokens", text)
            self.assertIn("total_tokens", text)
            self.assertIn("tool_calls", text)
            self.assertIn("| condition | metric | median | p90 | mean | n outputs |", text)

    def test_build_run_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.jsonl"
            subprocess.run([
                "python3", str(ROOT / "scripts/build_run_matrix.py"),
                "--case-ids", str(ROOT / "evals/smoke-case-ids.txt"),
                "--repeats", "1", "--out", str(out)
            ], check=True, capture_output=True, text=True)
            rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(24, len(rows))
            self.assertEqual({"baseline", "release"}, {r["condition"] for r in rows})

    def test_build_run_matrix_supports_scoped_competitor(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            ids = d / "ids.txt"
            out = d / "plan.jsonl"
            ids.write_text("core-002\n", encoding="utf-8")
            subprocess.run([
                "python3", str(ROOT / "scripts/build_run_matrix.py"),
                "--case-ids", str(ids),
                "--conditions", "baseline", "release", "adhd",
                "--repeats", "1", "--out", str(out)
            ], check=True, capture_output=True, text=True)
            rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(3, len(rows))
            prompts = {row["condition"]: row["run_prompt"] for row in rows}
            self.assertTrue(prompts["release"].startswith("$find-solutions "))
            self.assertTrue(prompts["adhd"].startswith("/adhd "))
            self.assertEqual(rows[[r["condition"] for r in rows].index("baseline")]["task_prompt"], prompts["baseline"])

    def test_build_fast_frontier_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.jsonl"
            subprocess.run([
                "python3", str(ROOT / "scripts/build_run_matrix.py"),
                "--cases", str(ROOT / "evals/fast-frontier/cases.jsonl"),
                "--case-ids", str(ROOT / "evals/fast-frontier/headline-case-ids.txt"),
                "--conditions", "current", "candidate",
                "--repeats", "1", "--out", str(out),
            ], check=True, capture_output=True, text=True)
            rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(12, len(rows))
            self.assertEqual({"current", "candidate"}, {r["condition"] for r in rows})
            self.assertEqual({False}, {r["requires_web"] for r in rows})
            self.assertTrue(all(r["run_prompt"].startswith("$find-solutions ") for r in rows))

    def test_installer_dry_run(self):
        result = subprocess.run([
            "python3", str(ROOT / "scripts/install.py"), "--target", "all", "--dry-run"
        ], check=True, capture_output=True, text=True)
        self.assertIn("codex:", result.stdout)
        self.assertIn("claude:", result.stdout)


if __name__ == "__main__":
    unittest.main()
