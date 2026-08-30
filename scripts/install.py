#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT
SKILL_SURFACE = ("SKILL.md", "agents", "references")


def destination(target: str, project: Path | None) -> Path:
    if project is not None:
        base = project.expanduser().resolve()
        return base / (".agents/skills" if target == "codex" else ".claude/skills") / "find-solutions"
    home = Path.home()
    return home / (".agents/skills" if target == "codex" else ".claude/skills") / "find-solutions"


def install_one(target: str, project: Path | None, force: bool, dry_run: bool) -> None:
    dest = destination(target, project)
    print(f"{target}: {SOURCE} -> {dest}")
    if dry_run:
        return
    if SOURCE.resolve() == dest.resolve():
        print(f"{target}: already installed at {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if not force:
            raise FileExistsError(f"{dest} already exists; use --force to replace it")
        shutil.rmtree(dest)
    dest.mkdir()
    for name in SKILL_SURFACE:
        source = SOURCE / name
        target = dest / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install find-solutions locally without network access")
    parser.add_argument("--target", choices=["codex", "claude", "all"], required=True)
    parser.add_argument("--project", type=Path, help="Install inside this project instead of the user home")
    parser.add_argument("--force", action="store_true", help="Replace an existing skill directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not SOURCE.exists():
        print(f"source skill is missing: {SOURCE}", file=sys.stderr)
        return 2
    targets = ["codex", "claude"] if args.target == "all" else [args.target]
    try:
        for target in targets:
            install_one(target, args.project, args.force, args.dry_run)
    except (OSError, FileExistsError) as exc:
        print(f"installation failed: {exc}", file=sys.stderr)
        return 1
    print("Installation complete. Restart the host if the skill is not immediately visible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
