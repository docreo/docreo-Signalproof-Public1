---
name: cli-debug-verify
description: Localize CLI defects, correct the smallest failing layer, rerun regression tests, and verify exact route, policy, installer, and response behavior before declaring success.
---

# CLI Debug and Verify

1. Reproduce the failure.
2. Identify the failing layer: parser, policy, registry, adapter, runtime, installer, or test.
3. Inspect prior failed attempts before retrying.
4. Make the smallest correction.
5. Rerun the failing test.
6. Rerun the full suite.
7. Verify a real user-path command when safe and available.

Regression checks: exact route identity, no silent fallback, transport boundary, missing-model failure, explicit install approval, response envelope, and launcher behavior.

Never claim installation, connection, or successful invocation unless runtime evidence was actually observed.
