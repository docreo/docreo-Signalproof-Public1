---
name: cli-plan
description: Convert the CLI objective into a bounded architecture, acceptance matrix, protected state, and implementation sequence before code changes begin.
---

# CLI Plan

Define:

- target users;
- supported commands;
- exact model routes;
- model capability modes;
- transport boundaries;
- credential approach;
- approval points;
- failure behavior;
- acceptance tests;
- rollback or last-known-good state.

Prefer the smallest release that proves the architecture.

At minimum test installation, route identity, missing-model behavior, inference, no-silent-fallback behavior, security boundaries, and machine-readable output.
