# Sanitization Report

Repository: `docreo/docreo-Signalproof-Public1`

This repository was created fresh and does not inherit Git history from the previous public repository.

## Included

- Signalproof Community CLI 0.2.0
- exact local Qwen3.6 and Granite 4.2 8B routes
- Build Your Own AI CLI guide
- generic starter template
- six CLI Builder skills
- public-boundary documentation
- automated sanitization CI
- Apache License 2.0 and third-party notices

## Explicitly excluded

- connected-site application data and website deltas
- private VPS/server routes and server inventories
- SSH identities, keys, credentials, tokens, or private connectors
- tenant/customer state
- internal development or assurance evidence
- private model-training state
- developer workstation paths, worktrees, quarantine/evidence paths, or mount locations
- private-network topology
- inherited authentication to private Signalproof infrastructure

## Runtime boundary

The Community CLI is local-only. It accepts only HTTP loopback model transport and has no route to private Signalproof infrastructure.

## Visual-parity update (Public1 V1/RD2)

- Public chat presentation and SVG preview now share the accepted gold/red wordmark and plain session layout. They do not include the rejected Sagittarius dashboard.
- All preview identity data is generic (`LOCAL USER`); the only model shown is the publicly supported local Granite tag. Live readiness is never invented: displayed initial state is `UNVERIFIED`.
- Public-only command vocabulary and `SP://COMMUNITY` are used. No protected Signal Keys, private Orchestrator implementation, infrastructure details, private logs or developer paths were imported.
- Public policy remains advisory-only and loopback-only; existing exact-route and transport code remains unchanged.
