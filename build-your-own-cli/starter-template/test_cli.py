from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("starter_cli", HERE / "cli.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class StarterCliTests(unittest.TestCase):
    def test_remote_transport_is_rejected(self):
        with self.assertRaises(MODULE.CliError):
            MODULE.validate_transport("https://example.com")

    def test_loopback_transport_is_allowed(self):
        MODULE.validate_transport("http://127.0.0.1:11434")

    def test_unknown_route_is_rejected(self):
        with self.assertRaises(MODULE.CliError):
            MODULE.exact_route("does-not-exist")

    def test_policy_disables_silent_fallback(self):
        self.assertFalse(MODULE.policy()["allow_silent_fallback"])


if __name__ == "__main__":
    unittest.main()
