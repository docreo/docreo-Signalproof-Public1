# Security and Public Sanitization

Signalproof Community CLI is intentionally local, bounded, and sanitized for public distribution.

## Enforced runtime boundary

- Model transport is HTTP loopback only: `127.0.0.1`, `localhost`, or `::1`.
- A configured URL outside loopback is rejected before inference.
- There are no public VPS routes.
- There is no SSH route, remote-server route, cloud-worker route, or private Signalproof route in this edition.
- There is no server discovery or internal route inventory.
- There is no inherited authentication from private Signalproof infrastructure.
- There are no bundled credentials, tokens, SSH identities, tenant credentials, or connector secrets.
- The model receives no filesystem, browser, credential, tool, or remote-server capability.
- No silent model fallback is implemented.
- Missing model downloads require explicit human approval.

## Filesystem privacy boundary

Public/customer-facing output must not reveal developer workstation locations.

The public repository and CLI must not publish or emit developer drive letters, absolute workstation paths, home-directory expansions, private repository/worktree locations, evidence/quarantine locations, SSH-key paths, server configuration paths, internal mount paths, or private connector configuration locations.

The installer may internally use the user's local Python and selected installation directory to create that user's launcher, but it does not print those resolved absolute paths.

## Remote access rule

This Community CLI has no remote infrastructure capability.

Any future feature that reaches a server, VPS, hosted worker, private API, or protected website must be implemented as a separate authenticated connection surface with explicit login, narrowly scoped authorization, no inherited private credentials, no implicit route access, no internal topology disclosure, explicit revocation/disconnect behavior, and fail-closed unauthenticated tests.

Until separately designed and accepted, remote access remains absent.
