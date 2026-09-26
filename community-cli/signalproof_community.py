#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlparse

PRODUCT = "Signalproof Community CLI"
VERSION = "0.2.0"
DEFAULT_OLLAMA_URL = os.environ.get("SIGNALPROOF_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")


@dataclass(frozen=True)
class ModelSpec:
    alias: str
    tag: str
    display_name: str


SUPPORTED_MODELS = {
    "qwen": ModelSpec("qwen", "qwen3.6:latest", "Signalproof Governed Qwen3.6"),
    "granite": ModelSpec("granite", "granite4.2:8b", "Signalproof Governed Granite 4.2 8B"),
}


class CommunityError(RuntimeError):
    pass


# Public-owned presentation data only. This uses no private CLI package,
# protected route, Signal Keys credential or internal installation state.
PUBLIC_WORDMARK = (
    "███████╗ ██╗  ██████╗  ███╗   ██╗  █████╗  ██╗      ██████╗  ██████╗   ██████╗   ██████╗  ███████╗",
    "██╔════╝ ██║ ██╔════╝  ████╗  ██║ ██╔══██╗ ██║      ██╔══██╗ ██╔══██╗ ██╔═══██╗ ██╔═══██╗ ██╔════╝",
    "███████╗ ██║ ██║  ███╗ ██╔██╗ ██║ ███████║ ██║      ██████╔╝ ██████╔╝ ██║   ██║ ██║   ██║ █████╗",
    "╚════██║ ██║ ██║   ██║ ██║╚██╗██║ ██╔══██║ ██║      ██╔═══╝  ██╔══██╗ ██║   ██║ ██║   ██║ ██╔══╝",
    "███████║ ██║ ╚██████╔╝ ██║ ╚████║ ██║  ██║ ███████╗ ██║      ██║  ██║ ╚██████╔╝ ╚██████╔╝ ██║",
    "╚══════╝ ╚═╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝      ╚═╝  ╚═╝  ╚═════╝   ╚═════╝  ╚═╝",
)
PUBLIC_ROW_COLORS = (
    "\x1b[1;38;2;255;228;86m",
    "\x1b[1;38;2;255;222;73m",
    "\x1b[38;2;255;204;41m",
    "\x1b[38;2;255;192;55m",
    "\x1b[38;2;207;136;55m",
    "\x1b[38;2;189;116;44m",
)


def render_community_header(alias: str, *, columns: int | None = None,
                            ansi: bool | None = None) -> str:
    """Owner-accepted plain CLI visual structure, using public local facts only."""
    if alias not in SUPPORTED_MODELS:
        raise ValueError("unsupported public model alias")
    if columns is None:
        columns = shutil.get_terminal_size(fallback=(100, 30)).columns
    columns = max(1, int(columns))
    if ansi is None:
        ansi = bool(getattr(sys.stdout, "isatty", lambda: False)()) and (
            "NO_COLOR" not in os.environ and os.environ.get("TERM", "") != "dumb"
        )
    reset = "\x1b[0m" if ansi else ""
    red = "\x1b[38;2;227;24;53m" if ansi else ""
    gold = "\x1b[1;38;2;255;211;49m" if ansi else ""
    rows = []
    if columns >= max(map(len, PUBLIC_WORDMARK)):
        rows.extend(
            (PUBLIC_ROW_COLORS[i] + line + reset) if ansi else line
            for i, line in enumerate(PUBLIC_WORDMARK)
        )
    else:
        rows.append(gold + "SIGNALPROOF" + reset)
    bar = red + ("═" * min(columns, 100)) + reset
    rows.extend((
        bar,
        gold + "SIGNALPROOF" + reset + "  " + red + "//" + reset
        + "  " + gold + "HUMAN-CONTROLLED AI SYSTEMS" + reset,
        red + "SP://COMMUNITY" + reset + "  //  "
        + gold + "COMMUNITY " + VERSION + reset + "  //  LOCAL ONLY",
        bar,
        "",
        " SIGNALPROOF COMMUNITY CLI",
        " OPERATOR     LOCAL USER",
        " TRANSPORT    LOOPBACK ONLY",
        " ROUTE        " + alias,
        " MODEL        " + SUPPORTED_MODELS[alias].tag,
        " STATE        UNVERIFIED (checked on first prompt)",
        "",
        "Commands: /exit  /quit",
        "No silent model failover. Advisory-only; no tool authority.",
    ))
    return "\n".join(rows)



def require_loopback(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise CommunityError("community local-model transport must remain HTTP loopback-only")


def request_json(base_url: str, path: str, *, method: str = "GET", payload: dict | None = None, timeout: int = 300) -> dict:
    require_loopback(base_url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base_url.rstrip("/") + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            value = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read(2048).decode("utf-8", errors="replace")
        raise CommunityError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise CommunityError(f"Ollama unavailable: {exc}") from exc
    if not isinstance(value, dict):
        raise CommunityError("Ollama returned a non-object response")
    return value


def inventory(base_url: str) -> dict[str, dict]:
    payload = request_json(base_url, "/api/tags", timeout=10)
    rows = payload.get("models")
    if not isinstance(rows, list):
        raise CommunityError("Ollama model inventory returned an invalid shape")
    result: dict[str, dict] = {}
    for row in rows:
        if isinstance(row, dict):
            name = str(row.get("name") or row.get("model") or "").strip()
            if name:
                result[name] = row
    return result


def model_report(base_url: str) -> list[dict]:
    available = inventory(base_url)
    report = []
    for spec in SUPPORTED_MODELS.values():
        row = available.get(spec.tag, {})
        report.append({
            "alias": spec.alias,
            "display_name": spec.display_name,
            "model": spec.tag,
            "installed": spec.tag in available,
            "digest": str(row.get("digest") or "") or None,
            "size": row.get("size"),
            "governance_mode": "NON_EXECUTING_ADVISORY",
            "direct_model_authority": False,
        })
    return report


def governed_advisory(base_url: str, alias: str, prompt: str, *, timeout: int = 900) -> dict:
    if alias not in SUPPORTED_MODELS:
        raise CommunityError("unsupported model alias; choose qwen or granite")
    if not isinstance(prompt, str) or not prompt.strip():
        raise CommunityError("prompt must be non-empty")

    spec = SUPPORTED_MODELS[alias]
    available = inventory(base_url)
    if spec.tag not in available:
        raise CommunityError(
            f"exact supported model is not installed: {spec.tag}. Run 'signalproof-community setup' or install it with Ollama."
        )
    digest = str(available[spec.tag].get("digest") or "").strip()
    if not digest:
        raise CommunityError(f"exact model digest is unavailable for {spec.tag}")

    system = (
        "You are operating inside Signalproof Community governed advisory mode. "
        "You may explain, analyze, draft, summarize, or recommend. "
        "You have no tool authority, no file authority, no browser authority, "
        "no credential authority, and no permission to claim an external action was executed. "
        "Treat the user's request as advisory-only and answer directly."
    )
    body = {
        "model": spec.tag,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt.strip()},
        ],
        "stream": False,
    }
    if alias == "qwen":
        body["think"] = False

    result = request_json(base_url, "/api/chat", method="POST", payload=body, timeout=timeout)
    message = result.get("message")
    if not isinstance(message, dict):
        raise CommunityError("model response did not contain a message object")
    answer = str(message.get("content") or "").strip()
    if not answer:
        raise CommunityError("model returned an empty final response")

    return {
        "product": PRODUCT,
        "version": VERSION,
        "route": alias,
        "model": spec.tag,
        "model_digest": digest,
        "governance_mode": "NON_EXECUTING_ADVISORY",
        "direct_model_authority": False,
        "browser_authority": False,
        "response": answer,
    }


def render_models(rows: list[dict]) -> None:
    print("Signalproof Community CLI - supported governed local models")
    print()
    for row in rows:
        marker = "READY" if row["installed"] else "NOT INSTALLED"
        print(f"{row['alias']:<8} {row['model']:<20} {marker}")
    print()
    print("No silent model substitution. Only the exact listed tags are accepted by this release.")


def confirm_download(spec: ModelSpec) -> bool:
    answer = input(f"Download {spec.tag} with Ollama now? [y/N]: ").strip().lower()
    return answer in {"y", "yes"}


def pull_model(spec: ModelSpec) -> None:
    executable = shutil.which("ollama")
    if not executable:
        raise CommunityError("Ollama CLI was not found on PATH. Install Ollama first, then run setup again.")
    print(f"Installing exact model route: {spec.alias} -> {spec.tag}")
    completed = subprocess.run([executable, "pull", spec.tag], check=False)
    if completed.returncode != 0:
        raise CommunityError(f"ollama pull failed for {spec.tag} with exit code {completed.returncode}")


def cmd_setup(args) -> int:
    available = inventory(args.ollama_url)
    aliases = [args.model] if args.model else list(SUPPORTED_MODELS)
    installed_any = False
    skipped_any = False

    for alias in aliases:
        spec = SUPPORTED_MODELS[alias]
        if spec.tag in available:
            print(f"READY: {alias} -> {spec.tag}")
            continue
        print(f"MISSING: {alias} -> {spec.tag}")
        if confirm_download(spec):
            pull_model(spec)
            installed_any = True
        else:
            print(f"SKIPPED: {spec.tag}")
            skipped_any = True

    if installed_any:
        print()
        print("Rechecking model inventory...")
        render_models(model_report(args.ollama_url))
    elif skipped_any:
        print("No model downloads were authorized.")
    else:
        print("All selected model routes are already installed.")
    return 0


def cmd_models(args) -> int:
    rows = model_report(args.ollama_url)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        render_models(rows)
    return 0


def cmd_status(args) -> int:
    rows = model_report(args.ollama_url)
    payload = {
        "product": PRODUCT,
        "version": VERSION,
        "ollama_url": args.ollama_url,
        "transport": "LOOPBACK_ONLY",
        "supported_models": rows,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        render_models(rows)
    return 0


def cmd_ask(args) -> int:
    result = governed_advisory(args.ollama_url, args.model, args.prompt, timeout=args.timeout)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["response"])
    return 0


def cmd_chat(args) -> int:
    print(render_community_header(args.model))
    while True:
        try:
            prompt = input(f"YOU [{args.model}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.lower() in {"/exit", "/quit", "exit", "quit"}:
            break
        if not prompt:
            continue
        try:
            result = governed_advisory(args.ollama_url, args.model, prompt, timeout=args.timeout)
            print(f"Signalproof [{args.model.upper()}] > {result['response']}")
        except CommunityError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=PRODUCT)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--json", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", help="check exact model routes and explicitly offer to download missing models")
    p.add_argument("--model", choices=sorted(SUPPORTED_MODELS), help="limit setup to one model route")
    p.set_defaults(func=cmd_setup)

    p = sub.add_parser("models", help="list exact supported governed local models and installation state")
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("status", help="show community CLI local-model readiness")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("ask", help="send one advisory prompt through an exact governed local model")
    p.add_argument("model", choices=sorted(SUPPORTED_MODELS))
    p.add_argument("prompt")
    p.add_argument("--timeout", type=int, default=900)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("chat", help="open a local advisory chat session")
    p.add_argument("model", choices=sorted(SUPPORTED_MODELS))
    p.add_argument("--timeout", type=int, default=900)
    p.set_defaults(func=cmd_chat)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        require_loopback(args.ollama_url)
        return args.func(args)
    except CommunityError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"status": "error", "error": str(exc)}))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
