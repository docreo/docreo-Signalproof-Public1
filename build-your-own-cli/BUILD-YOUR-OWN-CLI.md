# Build Your Own AI CLI

A step-by-step manual for building a local, multi-model command-line interface with explicit routing, bounded model authority, human approval points, verification, and release discipline.

This guide is based on lessons learned while building a working two-model CLI, but it intentionally describes the architecture in generic terms. It does not publish private infrastructure, private governance thresholds, credentials, server addresses, internal build records, or proprietary operational data.

## 1. Decide what the CLI is for

Do not start with code. Start with the operating contract.

Write down:

- who the human operator is;
- what models the CLI can reach;
- what each model is allowed to do;
- what the models are explicitly not allowed to do;
- whether the CLI is advisory-only or can call tools;
- where credentials live;
- which transports are allowed;
- what evidence must be produced;
- what happens when a route is unavailable;
- what requires human approval.

A safe first release is usually advisory-only. Let the model answer. Do not give it file, browser, shell, credential, purchasing, deployment, or remote-control authority until those capabilities have their own policy gates and tests.

## 2. Draw the architecture before implementing it

```text
HUMAN OPERATOR
      |
      v
CLI PARSER / COMMAND SURFACE
      |
      v
POLICY + APPROVAL GATE
      |
      v
ROUTE REGISTRY
      |
      v
MODEL ADAPTER
      |
      v
LOCAL OR REMOTE MODEL RUNTIME
      |
      v
RESPONSE ENVELOPE + EVIDENCE
      |
      v
HUMAN OPERATOR
```

The model is not the CLI. The model is one worker behind the CLI. Once the route registry, policy gate, and adapter layer are separate, you can replace or add models without rebuilding the entire command surface.

## 3. Pick a small runtime

Python is a strong first choice because it is cross-platform, readable, and easy to package.

A lightweight first version can use:

- `argparse` for commands;
- `urllib` for HTTP;
- `json` for configuration and payloads;
- `subprocess` only for tightly bounded external commands;
- `pathlib` for filesystem paths;
- `unittest` for tests.

You do not need a large framework to prove the architecture.

## 4. Create an exact model registry

Do not scatter model names through the code.

```python
SUPPORTED_MODELS = {
    "model-a": {"tag": "vendor-model-a:exact-tag", "mode": "ADVISORY"},
    "model-b": {"tag": "vendor-model-b:exact-tag", "mode": "ADVISORY"},
}
```

Each route should have a short alias, exact provider/runtime model identifier, display name, capability mode, transport boundary, and optional timeout/context settings.

Avoid fuzzy selection such as "use whatever version is available." Exact routing makes upgrades deliberate and testable.

## 5. Separate route selection from inference

The route resolver answers: which exact worker did the human select?

The adapter answers: how do I communicate with that worker?

Do not merge those responsibilities.

An unknown alias should fail before any model call.

## 6. Refuse silent fallback

If the operator selected `model-a` and it is unavailable, fail clearly.

Do not silently send the request to `model-b`.

If you later support fallback, make it explicit, such as `--fallback model-b`, and record that choice in the run evidence.

## 7. Add a readiness check before inference

Before a model receives a prompt, verify:

1. the runtime endpoint is reachable;
2. the endpoint is on an allowed network boundary;
3. the exact model tag is installed;
4. the runtime reports a stable model identity such as a digest;
5. the model route matches the registry.

"The server answered" is not the same as "the correct model is ready."

## 8. Put policy before the model call

A minimal policy might track:

```json
{
  "mode": "ADVISORY_ONLY",
  "allow_tools": false,
  "allow_filesystem": false,
  "allow_browser": false,
  "allow_credentials": false,
  "allow_remote_actions": false,
  "allow_silent_fallback": false
}
```

The policy should be enforced by code, not only written in a system prompt.

## 9. Keep model authority narrower than human authority

The human chooses the route and the action.

In an advisory CLI, the model may explain, summarize, classify, draft, analyze, and recommend. It should not claim external work was executed.

If tools are added later, expose them through a separate broker or capability layer. Do not give unrestricted shell access merely because the CLI itself can invoke processes.

## 10. Isolate credentials

If the first version is local-only, avoid credentials entirely.

When API providers are added later:

- use environment variables, OS credential storage, or a dedicated secret store;
- never hard-code tokens;
- never print raw credentials;
- never put secrets into model prompts or ordinary logs;
- keep credential ownership separate from route ownership.

## 11. Restrict transport deliberately

For a local-only first release, loopback-only transport is a strong boundary.

Accept loopback hosts. Reject arbitrary remote hosts unless remote access is part of the designed release.

Do not let configuration quietly turn a local route into a remote route without validation.

## 12. Create one-shot and interactive modes separately

One-shot:

```text
mycli ask model-a "Summarize this text"
```

Interactive:

```text
mycli chat model-a
```

Keep one-shot calls scriptable and interactive sessions human-friendly.

## 13. Add a setup command instead of guessing

Model weights can be large. Do not silently download them during installation.

Use a setup flow:

```text
mycli setup
```

The CLI should detect the runtime, inspect installed models, identify missing exact routes, ask the user before every download, call the runtime with a fixed argument vector, then re-check inventory.

Default the download prompt to no.

Prefer:

```python
subprocess.run([runtime_exe, "pull", exact_model_tag])
```

instead of building a shell command from arbitrary user text.

## 14. Surface model identity in the response

A trustworthy CLI should be able to say what actually answered.

```json
{
  "route": "model-a",
  "model": "vendor-model-a:exact-tag",
  "model_digest": "observed-runtime-digest",
  "mode": "ADVISORY_ONLY",
  "response": "..."
}
```

This makes debugging, comparison, testing, and audits easier.

## 15. Add a doctor/status surface

Useful commands include:

```text
mycli status
mycli models
mycli doctor
```

A doctor command can verify runtime version, operating system, binary availability, endpoint reachability, installed model routes, configuration validity, and optional credential presence without revealing secrets.

## 16. Treat tools as a second architecture phase

Do not confuse a multi-model CLI with an agent that has unrestricted tools.

A tool-capable architecture should look like:

```text
MODEL
  |
  v
TOOL REQUEST
  |
  v
POLICY CHECK
  |
  v
HUMAN APPROVAL WHEN REQUIRED
  |
  v
BOUNDED TOOL ADAPTER
  |
  v
RESULT + EVIDENCE
```

Validate arguments, capability scope, target, and side effects.

## 17. Build tests around boundaries, not just happy paths

Minimum tests should include:

- only known aliases are accepted;
- exact model tags are used;
- remote transport is rejected when local-only is required;
- missing models fail clearly;
- silent fallback does not occur;
- model downloads require explicit approval;
- download commands use fixed argument vectors;
- empty prompts fail;
- malformed runtime responses fail;
- machine-readable JSON stays stable;
- installer creates expected launchers.

Every real defect should become a regression test.

## 18. Package the CLI separately from model weights

A public pack should contain source, installer, tests, README, model-registry documentation, security documentation, license, third-party notices, a build-your-own guide, starter template, and optional skills.

Do not bundle multi-gigabyte model weights unless you have a deliberate redistribution plan and the applicable license allows it.

## 19. Keep third-party notices explicit

For every runtime, model, SDK, or dependency, record:

- component name;
- upstream owner;
- exact source/version/tag;
- license or terms;
- whether it is redistributed;
- whether it is modified;
- where it is used.

Your repository license does not overwrite a model's license.

## 20. Use Git as the release boundary

A disciplined flow is:

```text
research -> plan -> design -> build -> test -> review/security -> human acceptance -> release
```

Work on a branch. Preserve the last known-good state. Do not declare a release merely because the code imports.

A release candidate should have exact version identity, source commit, passing tests, security review, notice/license review, installation verification, rollback path, and human acceptance.

## 21. Add more models by adding routes, not rewriting the CLI

For each new model:

1. add one registry entry;
2. add or reuse an adapter;
3. define its capability policy;
4. define its exact runtime identifier;
5. add readiness checks;
6. add tests;
7. update license/notices;
8. pass acceptance before release.

Do not add a model to the public route list merely because it can produce text.

## 22. Example progression

```text
RD1  single local model, one-shot ask
RD2  interactive chat
RD3  exact route registry
RD4  second model route
RD5  no-silent-fallback tests
RD6  readiness/status surface
RD7  model digest/evidence
RD8  interactive model installer with explicit approval
RD9  public packaging and acceptance
```

Start the next version for materially expanded capabilities such as additional model families, remote providers, tools, or managed workers.

## 23. Recommended repository structure

```text
my-cli/
├── README.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
├── install.py
├── src/
│   └── my_cli/
│       ├── __init__.py
│       ├── cli.py
│       ├── registry.py
│       ├── policy.py
│       ├── adapters/
│       └── evidence.py
├── tests/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── MODELS.md
└── skills/
```

## 24. Governance without copying somebody else's governance system

At minimum, define your own answers for:

- **Identity:** who or what is acting?
- **Intent:** what outcome is requested?
- **Route:** which exact model/provider is selected?
- **Authority:** what actions may this route perform?
- **Data boundary:** what data may enter or leave?
- **Secrets:** which credentials may be referenced and by whom?
- **Approval:** which actions require explicit human approval?
- **Fallback:** prohibited or explicitly configured?
- **Budget:** what time, token, or cost limits apply?
- **Verification:** how will the system prove the requested thing happened?
- **Evidence:** what should be logged without leaking sensitive data?
- **Recovery:** how do you return to the last known-good state?

The implementation can be simple. The important part is making these decisions explicit and enforceable.

## 25. Where DSP-style skills fit

The companion skill pack breaks work into research, planning, route governance, build, debug/verification, and release.

If you use the public Signalproof Skills library, the closest DSP capability families include research, investigate, plan, grill, design, readiness, build, known-errors, debug, verify, review, recovery, security, secrets, permissions, network, execution-security, supply-chain, release, closeout, and document.

The important idea is not the command name. The important idea is that build, security, verification, and release are separate responsibilities with separate evidence.

## Final rule

Keep the model behind the boundary.

The CLI should know which worker was selected, what that worker is allowed to do, what actually ran, and when the human must decide. If you preserve those separations, you can grow from one local model to a multi-model operating surface without turning the command line into an uncontrolled collection of model calls.
