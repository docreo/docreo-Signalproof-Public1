# Supported Models

Signalproof Community CLI 0.2.0 currently enables these exact local routes.

## Qwen

- CLI alias: `qwen`
- Ollama tag: `qwen3.6:latest`
- route mode: `NON_EXECUTING_ADVISORY`
- direct model authority: `false`
- transport: local Ollama loopback only

## Granite

- CLI alias: `granite`
- Ollama tag: `granite4.2:8b`
- route mode: `NON_EXECUTING_ADVISORY`
- direct model authority: `false`
- transport: local Ollama loopback only

## Model setup

Run:

```text
signalproof-community setup
```

For each missing supported model, the CLI asks whether the user wants to run the corresponding exact `ollama pull` command. A declined model is not downloaded. There is no silent substitution.

## Not included in this revision

Gemma and Ministral are deliberately not part of this pack yet. They can be added as additional exact routes after their own acceptance, license review, tests, and release decision.

Cloud/API provider routes and private workers are also outside this sanitized local-only release.
