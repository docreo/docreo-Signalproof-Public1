#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py",
    ".ps1", ".cmd", ".bat", ".sh", ".js", ".ts", ".tsx", ".jsx",
    ".html", ".css", ".svg", ".xml", ".ini", ".cfg"
}

RULES = [
    ("connected-site data", re.compile(r"chudcon", re.IGNORECASE)),
    ("Windows user path", re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE)),
    ("Signalproof workstation drive path", re.compile(r"\bF:\\(?:SP|Downloads|ai-apps)\\", re.IGNORECASE)),
    ("Unix home path", re.compile(r"(?<![A-Za-z0-9_])/home/[A-Za-z0-9._-]+/")),
    ("private IPv4 10/8", re.compile(r"\b10(?:\.\d{1,3}){3}\b")),
    ("private IPv4 192.168/16", re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b")),
    ("private IPv4 172.16/12", re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b")),
    ("OpenSSH private key", re.compile(r"BEGIN OPENSSH PRIVATE KEY")),
    ("PEM private key", re.compile(r"BEGIN (?:RSA |EC |DSA )?PRIVATE KEY")),
    ("SSH public key material", re.compile(r"\bssh-(?:rsa|ed25519)\s+[A-Za-z0-9+/]{40,}={0,3}")),
]

EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == SELF:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        yield path

def main() -> int:
    failures = []
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in RULES:
            match = pattern.search(text)
            if match:
                failures.append((path.relative_to(ROOT), label, match.group(0)[:120]))

    if failures:
        print("PUBLIC SANITIZATION: FAIL")
        for path, label, sample in failures:
            print(f"- {path}: {label}: {sample!r}")
        return 1

    print("PUBLIC SANITIZATION: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
