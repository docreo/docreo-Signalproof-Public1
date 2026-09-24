#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DEFAULT_URL = "http://127.0.0.1:11434"


class CliError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CliError(f"expected object in {path.name}")
    return value


def models() -> dict:
    return load_json(ROOT / "models.json")


def policy() -> dict:
    return load_json(ROOT / "policy.json")


def validate_transport(base_url: str) -> None:
    parsed = urlparse(base_url)
    allowed = set(policy().get("allowed_hosts", []))
    if parsed.scheme != "http" or parsed.hostname not in allowed:
        raise CliError("transport is outside the configured boundary")


def request_json(base_url: str, path: str, payload: dict | None = None) -> dict:
    validate_transport(base_url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base_url.rstrip("/") + path, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            value = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise CliError(f"runtime request failed: {exc}") from exc
    if not isinstance(value, dict):
        raise CliError("runtime returned an invalid response shape")
    return value


def inventory(base_url: str) -> dict[str, dict]:
    payload = request_json(base_url, "/api/tags")
    rows = payload.get("models")
    if not isinstance(rows, list):
        raise CliError("runtime model inventory is invalid")
    result = {}
    for row in rows:
        if isinstance(row, dict):
            name = str(row.get("name") or row.get("model") or "").strip()
            if name:
                result[name] = row
    return result


def exact_route(alias: str) -> dict:
    registry = models()
    if alias not in registry:
        raise CliError(f"unknown route: {alias}")
    route = registry[alias]
    if not isinstance(route, dict) or not str(route.get("tag") or "").strip():
        raise CliError(f"invalid route configuration: {alias}")
    return route


def ask(base_url: str, alias: str, prompt: str) -> dict:
    if not prompt.strip():
        raise CliError("prompt must not be empty")
    rules = policy()
    if rules.get("allow_silent_fallback"):
        raise CliError("starter template expects silent fallback to remain disabled")

    route = exact_route(alias)
    tag = str(route["tag"])
    available = inventory(base_url)
    if tag not in available:
        raise CliError(f"exact model is not installed: {tag}")
    digest = str(available[tag].get("digest") or "").strip() or None

    system = (
        "Operate in advisory-only mode. Do not claim tool, file, browser, credential, "
        "or external-action authority. Answer the user's request directly."
    )
    payload = {
        "model": tag,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt.strip()},
        ],
        "stream": False,
    }
    result = request_json(base_url, "/api/chat", payload)
    message = result.get("message")
    if not isinstance(message, dict):
        raise CliError("model response is missing message")
    answer = str(message.get("content") or "").strip()
    if not answer:
        raise CliError("model response is empty")
    return {
        "route": alias,
        "model": tag,
        "model_digest": digest,
        "mode": rules.get("mode", "ADVISORY_ONLY"),
        "response": answer,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic exact-route AI CLI starter")
    parser.add_argument("--url", default=DEFAULT_URL)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("models")
    p.set_defaults(kind="models")

    p = sub.add_parser("ask")
    p.add_argument("route", choices=sorted(models()))
    p.add_argument("prompt")
    p.set_defaults(kind="ask")

    args = parser.parse_args()
    try:
        validate_transport(args.url)
        if args.kind == "models":
            print(json.dumps(models(), indent=2, sort_keys=True))
        else:
            print(json.dumps(ask(args.url, args.route, args.prompt), indent=2, sort_keys=True))
        return 0
    except CliError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
