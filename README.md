# Signalproof Public

Fresh sanitized public distribution repository for Signalproof Community CLI and the Build Your Own AI CLI learning pack.

This repository was created from an explicit public whitelist. It does **not** inherit Git history from the previous public repository.

## Public boundary

This repository contains no authorized route to private Signalproof servers, VPS workers, SSH surfaces, credentials, connectors, tenant state, internal evidence, model-training state, or developer-machine filesystem locations.

Public applications do not inherit private Signalproof access.

The current Community CLI is local-only and may communicate only with a local Ollama runtime over HTTP loopback.

See [PUBLIC-BOUNDARY.md](PUBLIC-BOUNDARY.md).

## Signalproof CLI preview

![Signalproof CLI preview](docs/assets/signalproof-cli-preview.webp)

The public preview is intentionally cropped so it does not expose developer-machine filesystem locations.

## Community CLI

Current exact local routes:

- `qwen` -> `qwen3.6:latest`
- `granite` -> `granite4.2:8b`

The CLI is advisory-only, uses exact-route selection, rejects silent fallback, exposes no model tool authority, and asks before optional model downloads.

Quick start:

```text
cd community-cli
python install.py
signalproof-community setup
signalproof-community status
signalproof-community chat qwen
```

Model weights are not bundled.

## Build Your Own AI CLI

The companion guide explains how to build a multi-model CLI with explicit routing, bounded model authority, human approval gates, transport restrictions, verification, release discipline, and reusable CLI-builder skills.

Start with:

`build-your-own-cli/BUILD-YOUR-OWN-CLI.md`

## Sanitization

Every push and pull request runs `tools/check_public_sanitization.py`.

The gate rejects common public-boundary violations including connected-site data, workstation paths, private-network addresses, and private-key material.

## License

Unless a file states otherwise, Signalproof-authored code and documentation in this repository are licensed under Apache License 2.0. Third-party models and software retain their own upstream licenses and terms.

Copyright 2026 Doc Reo / Signalproof.
