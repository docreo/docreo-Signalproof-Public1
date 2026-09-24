---
name: cli-build
description: Implement the approved CLI plan with the smallest effective change while preserving working state and keeping model adapters, policy, routing, and command parsing separate.
---

# CLI Build

1. Confirm current branch and known-good baseline.
2. Re-read the accepted plan and route contract.
3. Implement the smallest bounded feature.
4. Add tests with the feature.
5. Run tests before opening the next feature.
6. Preserve working launchers/routes unless the plan explicitly changes them.
7. Do not add hidden fallbacks, downloads, or credential behavior.
8. Record changed files and test results.

Stop when a material architecture change appears that is not covered by the plan.
