# Public Distribution Boundary

This repository is a sanitized public distribution surface.

## Never publish here

- connected-site application data or deltas;
- private Signalproof server/VPS routes or server inventories;
- SSH identities, keys, tokens, credentials, or connector secrets;
- private tenant/customer configuration;
- internal Build Ledger or Assurance evidence;
- private model-training state;
- developer workstation drive paths, home paths, worktrees, quarantine/evidence paths, or mount locations;
- private-network addresses or internal topology;
- implicit routes to private Signalproof infrastructure.

## Public connection rule

A public application or CLI has no inherited access to Signalproof private infrastructure.

Any future remote connection must be a separately designed surface that requires explicit authentication/login, a narrowly scoped authorization grant, and fail-closed behavior when unauthenticated. Public code must not contain a pre-authorized route to private servers.

## Local path rule

Public/customer-visible output must not expose developer-machine filesystem locations. Local launchers may internally reference the installing user's own local runtime paths, but those resolved paths should not be emitted into public logs, documentation, or command output.

## Enforcement

`tools/check_public_sanitization.py` runs in CI and blocks common public-boundary violations.
