from __future__ import annotations

import importlib.util
import io
import os
from contextlib import redirect_stdout
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parent / "signalproof_community.py"
SPEC = importlib.util.spec_from_file_location("signalproof_community", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CommunityCliTests(unittest.TestCase):
    def test_supported_models_are_exact(self):
        self.assertEqual(MODULE.SUPPORTED_MODELS["qwen"].tag, "qwen3.6:latest")
        self.assertEqual(MODULE.SUPPORTED_MODELS["granite"].tag, "granite4.2:8b")

    def test_loopback_is_required(self):
        for url in (
            "http://127.0.0.1:11434",
            "http://localhost:11434",
            "http://[::1]:11434",
        ):
            MODULE.require_loopback(url)
        with self.assertRaises(MODULE.CommunityError):
            MODULE.require_loopback("https://example.com")

    def test_parser_exposes_only_supported_model_aliases(self):
        parser = MODULE.build_parser()
        for alias in ("qwen", "granite"):
            args = parser.parse_args(["ask", alias, "hello"])
            self.assertEqual(args.model, alias)

    def test_setup_parser_supports_optional_exact_route(self):
        parser = MODULE.build_parser()
        args = parser.parse_args(["setup", "--model", "qwen"])
        self.assertEqual(args.model, "qwen")

    def test_confirm_download_defaults_to_no(self):
        with patch("builtins.input", return_value=""):
            self.assertFalse(MODULE.confirm_download(MODULE.SUPPORTED_MODELS["qwen"]))
        with patch("builtins.input", return_value="yes"):
            self.assertTrue(MODULE.confirm_download(MODULE.SUPPORTED_MODELS["qwen"]))

    def test_pull_model_uses_fixed_argument_vector(self):
        spec = MODULE.SUPPORTED_MODELS["granite"]
        with patch.object(MODULE.shutil, "which", return_value="/usr/bin/ollama"), patch.object(MODULE.subprocess, "run") as run:
            run.return_value.returncode = 0
            MODULE.pull_model(spec)
            run.assert_called_once_with(["/usr/bin/ollama", "pull", "granite4.2:8b"], check=False)


    def test_accepted_plain_public_visual(self):
        result = MODULE.render_community_header("granite", columns=120, ansi=False)
        self.assertIn("SIGNALPROOF COMMUNITY CLI", result)
        self.assertIn("SP://COMMUNITY", result)
        self.assertIn("granite4.2:8b", result)
        self.assertIn("LOOPBACK ONLY", result)
        self.assertIn("UNVERIFIED", result)
        self.assertEqual(sum("███████" in line for line in result.splitlines()) >= 1, True)
        self.assertNotIn("\x1b", result)
        self.assertNotIn("GAdmin", result)

    def test_chat_uses_public_header_and_accurate_commands(self):
        out = io.StringIO()
        args = MODULE.build_parser().parse_args(["chat", "qwen"])
        with patch("builtins.input", side_effect=["/exit"]) as read, redirect_stdout(out):
            self.assertEqual(args.func(args), 0)
        shown = out.getvalue()
        self.assertIn("SIGNALPROOF COMMUNITY CLI", shown)
        self.assertIn("qwen3.6:latest", shown)
        self.assertIn("Commands: /exit  /quit", shown)
        read.assert_called_once_with("YOU [qwen] > ")

    def test_narrow_and_color_modes(self):
        short = MODULE.render_community_header("qwen", columns=55, ansi=False)
        self.assertNotIn("███████", short)
        self.assertIn("SIGNALPROOF", short)
        bright = MODULE.render_community_header("qwen", columns=120, ansi=True)
        self.assertIn("\x1b[", bright)
        self.assertIn("HUMAN-CONTROLLED AI SYSTEMS", bright)
        self.assertNotIn("READY", bright)  # Display only; no invented live state.


if __name__ == "__main__":
    unittest.main()
