"""Register an explicitly selected, user-confirmed figure recipe in a custom library."""

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(directory, relative):
    value = Path(relative)
    if value.is_absolute() or ".." in value.parts:
        raise ValueError("Library filenames must be relative and cannot contain ..")
    target = (directory / value).resolve()
    if not target.is_relative_to(directory.resolve()):
        raise ValueError("Library filename escapes its destination")
    return target


def load_spec(path, library):
    path = path.resolve()
    spec = json.loads(path.read_text(encoding="utf-8-sig"))
    if spec.get("schema_version") != 1:
        raise ValueError("Expected schema_version=1")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", spec.get("id", "")):
        raise ValueError("id must be a short lowercase ASCII identifier")
    if spec.get("user_confirmed") is not True:
        raise ValueError("Register only a figure or recipe the user has confirmed")
    if spec.get("data_status") not in ("synthetic", "approximate", "research", "none"):
        raise ValueError(
            "Specify synthetic, approximate, research, or none for data_status"
        )
    if not spec.get("title") or not spec.get("backend"):
        raise ValueError("title and backend are required")
    if not spec.get("files"):
        raise ValueError(
            "Provide explicit files; recursive directory import is not supported"
        )
    entry = inside(library, spec["id"])
    if entry.exists():
        raise FileExistsError(
            "Library entry already exists; choose a new id or edit the intended files explicitly"
        )
    resources, targets = [], set()
    for item in spec["files"]:
        source = (path.parent / item["source"]).resolve()
        if not source.is_file():
            raise FileNotFoundError("A selected library source file is missing")
        target = inside(entry, item["target"])
        if target.name == "entry.json" or target in targets:
            raise ValueError("Duplicate or reserved library target")
        targets.add(target)
        resources.append((source, target, item.get("role", "resource"), digest(source)))
    return spec, entry, resources


def register(path, library, check_only=False):
    spec, entry, resources = load_spec(path, library)
    if check_only:
        return {
            "valid": True,
            "id": spec["id"],
            "files": len(resources),
            "outputs_written": False,
        }
    entry.mkdir(parents=True, exist_ok=False)
    records = []
    for source, target, role, expected in resources:
        if digest(source) != expected:
            raise ValueError("Selected source changed during registration")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if digest(target) != expected:
            raise ValueError("Copied resource checksum differs")
        records.append(
            {
                "file": target.relative_to(entry).as_posix(),
                "role": role,
                "sha256": expected,
            }
        )
    metadata = {key: value for key, value in spec.items() if key != "files"}
    metadata["files"] = records
    (entry / "entry.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "registered": True,
        "id": spec["id"],
        "files": len(records),
        "data_status": spec["data_status"],
    }


def inspect_library(library):
    records = []
    for path in sorted(library.glob("*/entry.json")):
        spec = json.loads(path.read_text(encoding="utf-8-sig"))
        valid = all(
            digest(inside(path.parent, item["file"])) == item["sha256"]
            for item in spec["files"]
        )
        if not valid:
            raise ValueError(f"Library resource changed: {spec['id']}")
        records.append(
            {
                "id": spec["id"],
                "title": spec["title"],
                "backend": spec["backend"],
                "data_status": spec["data_status"],
                "files": len(spec["files"]),
                "hashes_valid": valid,
            }
        )
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library-dir", type=Path, default=ROOT / "figure-library")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--spec", type=Path)
    choice.add_argument("--list", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result = (
        inspect_library(args.library_dir)
        if args.list
        else register(args.spec, args.library_dir, args.check_only)
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
