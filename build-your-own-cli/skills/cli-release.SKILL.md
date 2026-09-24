---
name: cli-release
description: Prepare a CLI release candidate with exact version identity, passing tests, security and license review, sanitized packaging, human acceptance, and a rollback reference.
---

# CLI Release

Confirm:

- exact source branch/commit;
- release version;
- tests passing;
- security boundary review complete;
- secrets inspection complete;
- no machine-specific private paths in public files;
- third-party notices current;
- model weights intentionally excluded or legally distributable;
- installer tested;
- documentation matches behavior;
- previous known-good release remains recoverable.

Output a release artifact plus a manifest of included, excluded, verified, and planned items.
