"""Forward commands to the host's managed PaperSpine V6 installation."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def installation(skills_root):
    """Resolve the host pointer and the installed, bundled interpreter."""
    root = skills_root.expanduser().resolve()
    pointer_file = root / "paper-spine" / "installation.json"
    try:
        pointer = json.loads(pointer_file.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ValueError(
            f"No managed PaperSpine installation at {pointer_file}. "
            "Install the official V6 edition; embedded writing methods work offline."
        ) from exc
    if Path(pointer["skills_root"]).resolve() != root:
        raise ValueError("PaperSpine Skill pointer belongs to another skills root")
    manager = Path(pointer["manager"]).resolve()
    if not manager.is_file():
        raise ValueError(f"Installed PaperSpine manager is missing: {manager}")
    metadata_file = manager.parent / "active" / "edition.json"
    metadata = json.loads(metadata_file.read_text(encoding="utf-8-sig"))
    if metadata.get("format") != "paperspine-editions/1":
        raise ValueError("Unsupported PaperSpine installation format")
    bundled = (
        manager.parent / "active" / "runtime" / "runtime_vendor"
        / "windows-py312" / "python.exe"
    )
    interpreter = str(bundled) if bundled.is_file() else sys.executable
    return root, manager, interpreter, metadata


def main():
    default_root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=default_root)
    parser.add_argument("--describe", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        root, manager, interpreter, metadata = installation(args.skills_root)
        if args.describe:
            print(json.dumps({
                "version": metadata["version"], "edition": metadata["edition"],
                "manager": str(manager), "skills_root": str(root),
                "python": interpreter,
            }, ensure_ascii=False, indent=2))
            return 0
        command = args.command or ["status"]
        if command[0] not in {"status", "check", "preflight", "web"}:
            raise ValueError("Use status, check, preflight or web; upgrades use the official manager")
        if command[0] == "web" and metadata["edition"] != "web-plugin":
            raise ValueError("The installed edition has no Web runtime")
        return subprocess.call([
            interpreter, "-B", "-X", "utf8", str(manager),
            "--skills-root", str(root), *command,
        ])
    except (OSError, ValueError, KeyError) as exc:
        print(f"PaperSpine: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
