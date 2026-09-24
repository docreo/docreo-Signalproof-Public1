---
name: cli-route-governance
description: Design and review exact model routing, capability boundaries, approval gates, transport restrictions, credential separation, and evidence for an AI CLI.
---

# CLI Route Governance

## Core rules

1. Human selection resolves to one exact route.
2. Unknown or unavailable routes fail clearly.
3. Silent fallback is off unless explicitly designed and recorded.
4. Models receive only the capabilities required by the route.
5. Credentials remain outside prompts and ordinary logs.
6. Network targets are validated before connection.
7. Consequential actions require a separate capability and approval gate.
8. Response metadata identifies the route/model that actually answered.

## Review

Ask whether a model can change its own route, inherit another route's tools, leak credentials, cross a network boundary, or silently succeed through another provider.
