#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "find-solutions-v0.1.0.zip"


def main() -> int:
    subprocess.run(["python3", str(ROOT / "scripts/validate_repo.py")], check=True)
    subprocess.run(["python3", "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"], check=True, cwd=ROOT)
    DIST.mkdir(exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if rel.parts and rel.parts[0] in {"dist", "__pycache__", ".skill-forge"}:
                continue
            if "__pycache__" in rel.parts or path.suffix == ".pyc":
                continue
            zf.write(path, Path("find-solutions") / rel)
        # The repository keeps one physical active skill at its root. The plugin
        # archive additionally exposes that same surface at Codex's required
        # `skills/find-solutions` discovery path.
        for path in [ROOT / "SKILL.md", *(ROOT / "agents").rglob("*"), *(ROOT / "references").rglob("*")]:
            if path.is_file():
                rel = path.relative_to(ROOT)
                zf.write(path, Path("find-solutions") / "skills" / "find-solutions" / rel)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
