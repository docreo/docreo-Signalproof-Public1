# Generic Multi-Model CLI Starter

This is a deliberately small teaching template. It is not a Signalproof-branded runtime and it does not include private Signalproof components.

## Files

- `cli.py` - parser, exact route registry, loopback validation, Ollama adapter, and response envelope.
- `models.json` - exact route definitions.
- `policy.json` - default authority boundary.
- `test_cli.py` - boundary tests.

## Start

1. Edit `models.json` with exact model tags you have the right to use.
2. Keep `policy.json` restrictive while learning the architecture.
3. Run `python cli.py models`.
4. Run `python -m unittest test_cli.py -v`.
5. Add tools only after you have a separate capability and approval layer.
