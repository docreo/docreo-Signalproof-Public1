#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

MIN_PYTHON = (3, 11)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def install(target: Path) -> None:
    if sys.version_info < MIN_PYTHON:
        fail("Python 3.11+ is required")
    root = Path(__file__).resolve().parent
    source = root / "signalproof_community.py"
    if not source.is_file():
        fail("community CLI source file is missing")

    target.mkdir(parents=True, exist_ok=True)
    bin_dir = target / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    destination = target / "signalproof_community.py"
    shutil.copy2(source, destination)

    python = str(Path(sys.executable).resolve())
    if os.name == "nt":
        launcher = "@echo off\r\n" + f'"{python}" "{destination}" %*\r\n'
        (bin_dir / "signalproof-community.cmd").write_text(launcher, encoding="utf-8", newline="")
    else:
        launcher = "#!/bin/sh\n" + f'exec "{python}" "{destination}" "$@"\n'
        path = bin_dir / "signalproof-community"
        path.write_text(launcher, encoding="utf-8", newline="\n")
        path.chmod(0o755)

    print("Signalproof Community CLI installed.")
    print("No private routes, server connections, credentials, or filesystem locations were exposed.")
    print("Next: run 'signalproof-community setup' to check local model readiness.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install Signalproof Community CLI")
    parser.add_argument("--target", default=str(Path.home() / ".signalproof-community"))
    args = parser.parse_args(argv)
    install(Path(args.target).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
