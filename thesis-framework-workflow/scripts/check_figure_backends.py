"""Read-only capability probe for embedded Python/R drawing, without installing packages."""

import argparse
import importlib.metadata
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path


def python_status():
    required = {"numpy": "numpy", "matplotlib": "matplotlib"}
    optional = {"seaborn": "seaborn", "PyMuPDF": "fitz"}
    installed = {}
    for distribution, module in {**required, **optional}.items():
        found = importlib.util.find_spec(module) is not None
        try:
            version = importlib.metadata.version(distribution) if found else None
        except importlib.metadata.PackageNotFoundError:
            version = "present-version-unknown"
        installed[distribution] = version
    return {
        "runtime": "available",
        "packages": installed,
        "missing_core": [name for name in required if installed[name] is None],
        "missing_optional_or_qa": [
            name for name in optional if installed[name] is None
        ],
        "graphics_device_opened": False,
    }


def r_status(executable=None):
    command = executable or shutil.which("Rscript")
    if not command:
        return {
            "runtime": "not_found",
            "native_render_tested": False,
            "packages": "not_probed",
        }
    expression = (
        'p<-c("ggplot2","patchwork","jsonlite","svglite","ragg","ComplexHeatmap","circlize");'
        'for(n in p)cat(n,"=",if(requireNamespace(n,quietly=TRUE))'
        'as.character(utils::packageVersion(n)) else "MISSING","\\n",sep="")'
    )
    process = subprocess.run(
        [str(command), "--vanilla", "-e", expression],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if process.returncode:
        return {
            "runtime": "probe_failed",
            "exit_code": process.returncode,
            "packages": "not_probed",
        }
    packages = dict(
        row.split("=", 1) for row in process.stdout.splitlines() if "=" in row
    )
    return {
        "runtime": "available",
        "packages": packages,
        "graphics_device_opened": False,
        "native_render_tested": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["python", "r", "all"], default="all")
    parser.add_argument("--rscript", type=Path)
    args = parser.parse_args()
    result = {}
    if args.backend in ("python", "all"):
        result["python"] = python_status()
    if args.backend in ("r", "all"):
        result["r"] = r_status(args.rscript)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
