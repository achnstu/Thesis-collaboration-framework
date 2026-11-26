"""Read-only package, privacy and capability checks, independent of the cwd."""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import struct
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bar_line_inputs import load_manifest as load_bar_line_manifest
from waterfall_inputs import load_manifest

ROOT = Path(__file__).resolve().parents[1]
TEXT = {".md", ".py", ".ps1", ".sh", ".json", ".yaml", ".yml", ".txt", ".csv", ".toml"}
PRIVATE = re.compile(
    r"(?:[A-Za-z]:[/\\]Users[/\\](?!Public\b|Default\b)[^/\\\s]+|"
    r"(?:/Users|/home)/[a-z][^/\s]+|"
    r"01a[0-9a-f]{5}-[0-9a-f-]{27}|\bMid\d+[A-Za-z0-9]*\b|\bC[1-9][-_]D\d{2}\b)"
)


def markdown_links(path):
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Inline Markdown examples describe caller-owned assets, not package links.
    text = re.sub(r"`+[^`\n]*`+", "", text)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().strip("<>")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        if any(marker in target for marker in ("{", "<", "*", "$")):
            continue
        yield target.split("#", 1)[0]


def check_links():
    missing = []
    count = 0
    files = ROOT.rglob("*.md")
    for path in files:
        for target in markdown_links(path):
            count += 1
            if not (path.parent / target).exists():
                missing.append(
                    {"file": path.relative_to(ROOT).as_posix(), "target": target}
                )
    return count, missing


def scan_private():
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(
            p in (".venv", ".git", "__pycache__") for p in path.parts
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeError:
            continue
        if PRIVATE.search(text):
            findings.append(path.relative_to(ROOT).as_posix())
    return findings


def capabilities():
    installed = {}
    for name in ("numpy", "pandas", "pillow", "originpro", "OriginExt"):
        try:
            installed[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed[name] = None
    return {
        "system": platform.system(),
        "python": platform.python_version(),
        "architecture_bits": struct.calcsize("P") * 8,
        "packages": installed,
        "native_origin_platform": platform.system() == "Windows",
        "origin_handshake": "not_attempted",
        "word_display": "not_checked",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    required = [
        "SKILL.md",
        "references/portability.md",
        "scripts/render_waterfall.py",
        "references/academic-tables.md",
        "references/word-tooling.md",
        "references/revision-workflow.md",
        "references/writing-examples.md",
        "references/writing.md",
        "embedded/humanizer-zh/SKILL.md",
        "embedded/lieflat-less-ai-tone/SKILL.md",
        "embedded/lieflat-less-ai-tone/LICENSE",
        "scripts/build_table_example.py",
        "assets/templates/two-level-three-line-table.docx",
        "assets/templates/two-level-three-line-table.png",
        "examples/waterfall/manifest.json",
        "assets/waterfall/perspective-example.png",
        "assets/waterfall/label-detail.png",
        "references/origin-bar-line-dual-axis.md",
        "references/bar-line-dual-axis-validation.json",
        "scripts/render_bar_line_dual_axis.py",
        "scripts/origin_bar_line_style.py",
        "scripts/verify_bar_line_dual_axis.py",
        "scripts/bar_line_inputs.py",
        "examples/bar-line-dual-axis/manifest.json",
        "examples/bar-line-dual-axis/totals.csv",
        "examples/bar-line-dual-axis/curves.csv",
        "assets/bar-line-dual-axis/example.png",
        "embedded/editaplot/LICENSE",
        "embedded/editaplot/runtime/src/origin_sciplot/origin_backend/session.py",
        "embedded/editaplot/runtime/templates",
        "figure-library/INDEX.md",
        "figure-library/perspective-waterfall/entry.json",
        "figure-library/bar-line-dual-axis/entry.json",
        "scripts/register_figure_example.py",
        "scripts/check_figure_backends.py",
        "references/python-r-figures.md",
        "embedded/nature-figure/LICENSE",
        "embedded/nature-figure/PROVENANCE.json",
        "embedded/nature-figure/manifest.yaml",
        "embedded/nature-figure/scripts/plot_templates.py",
        "embedded/nature-figure/scripts/panel_alignment.R",
        "embedded/nature-figure/static/fragments/backend/python.md",
        "embedded/nature-figure/static/fragments/backend/r.md",
        "examples/nature-r/render_example.R",
    ]
    missing = [name for name in required if not (ROOT / name).exists()]
    count, links = check_links()
    private = scan_private()
    panels = []
    source_hashes_ok = False
    sample_error = None
    bar_line = {}
    try:
        _, panels, hashes = load_manifest(ROOT / "examples/waterfall/manifest.json")
        source_hashes_ok = all(
            hashlib.sha256(Path(p).read_bytes()).hexdigest() == value
            for p, value in hashes.items()
        )
        config, bars, curves, _ = load_bar_line_manifest(
            ROOT / "examples/bar-line-dual-axis/manifest.json"
        )
        bar_line = {
            "synthetic": config.get("synthetic", False),
            "categories": len(bars["values"]),
            "curves": len(curves),
            "points": sum(len(curve["x"]) for curve in curves),
        }
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Avoid placing source paths or CSV contents in shareable diagnostics.
        sample_error = type(exc).__name__
    from register_figure_example import inspect_library

    library_error = None
    try:
        library = inspect_library(ROOT / "figure-library")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        library, library_error = [], type(exc).__name__
    report = {
        "ok": not (missing or links or private or sample_error or library_error)
        and source_hashes_ok,
        "missing_resources": missing,
        "relative_links_checked": count,
        "broken_core_links": links,
        "private_path_or_session_files": private,
        "sample": {
            "synthetic": True,
            "series": len(panels),
            "points": sum(len(p["x"]) for p in panels),
            "source_hashes_valid": source_hashes_ok,
            "error_type": sample_error,
        },
        "capabilities": capabilities(),
        "bar_line_dual_axis_sample": bar_line,
        "user_figure_library": {"entries": library, "error_type": library_error},
        "origin_started": False,
        "outputs_written": False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
