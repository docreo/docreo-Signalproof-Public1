# Signalproof Community CLI

Free, sanitized, local-only community edition of the Signalproof command-line model surface.

This public edition is intentionally smaller than the private Signalproof engineering runtime. It contains no private server addresses, SSH identities, tenant configuration, private connectors, internal build records, private model-training state, or proprietary credentials.

## What it runs today

| CLI alias | Exact Ollama tag | Mode |
| --- | --- | --- |
| `qwen` | `qwen3.6:latest` | Governed non-executing advisory |
| `granite` | `granite4.2:8b` | Governed non-executing advisory |

Both routes are explicit. There is no silent substitution to another model.

## Requirements

- Python 3.11 or newer
- Ollama installed and running locally on `127.0.0.1:11434`
- enough disk/RAM for whichever supported model the user chooses

The model weights are not bundled.

## Install

```text
python install.py
```

On Windows, the launcher is created under:

```text
%USERPROFILE%\.signalproof-community\bin
```

## Guided model setup

```text
signalproof-community setup
```

For each missing route, the CLI asks before running the exact `ollama pull` command. The default answer is no.

To check only one route:

```text
signalproof-community setup --model qwen
signalproof-community setup --model granite
```

Manual installation remains available:

```text
ollama pull qwen3.6:latest
ollama pull granite4.2:8b
```

## Use

```text
signalproof-community models
signalproof-community status
signalproof-community ask qwen "Explain the difference between a model and a model route."
signalproof-community ask granite "Summarize this paragraph."
signalproof-community chat qwen
signalproof-community chat granite
```

## Governance boundary

The public community edition is deliberately advisory-only:

- exact route selection
- no silent fallback
- local loopback-only transport
- exact model digest surfaced
- no bundled secrets
- no remote server control
- no private connectors
- no model tool authority
- explicit human approval before optional model downloads

This is an execution boundary around upstream models. It is not a claim that the models were retrained or modified by Signalproof.

## Learn to build your own

See `../build-your-own-cli/BUILD-YOUR-OWN-CLI.md`.

## Status

Community release: **0.2.0**

Pack revision: **V1/RD1**
