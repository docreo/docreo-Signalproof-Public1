# CLI Architecture Reference

## Minimal control stack

```text
Human
  |
  v
Command Parser
  |
  v
Policy / Approval Gate
  |
  v
Exact Route Registry
  |
  v
Provider or Runtime Adapter
  |
  v
Model
  |
  v
Verified Response Envelope
  |
  v
Human
```

## Responsibility separation

| Layer | Owns | Must not silently own |
| --- | --- | --- |
| Parser | command syntax and validation | model selection policy |
| Policy gate | capability/approval decisions | provider transport |
| Route registry | alias to exact model identity | credentials |
| Adapter | runtime/API translation | human authorization |
| Model | inference | external authority |
| Evidence | observed route/result metadata | invented success claims |

## Recommended invariants

1. An unknown route fails before inference.
2. A missing exact model fails instead of silently substituting another model.
3. Transport is validated before connection.
4. Credentials are not embedded in source or prompts.
5. Tool authority is false unless explicitly granted by a separate capability layer.
6. Model identity is observable in status or response metadata.
7. Download/install actions require human approval.
8. Release state is proven by tests and exact source identity.
