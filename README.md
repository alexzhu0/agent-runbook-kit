# Agent Runbook Kit

Generate a minimal runbook kit for AI agent repositories.

## Why

Agent projects often lack release, eval, and launch checklists.

This repository is intentionally small: it should be useful in one command, easy to inspect, and simple to fork.

## Install

```bash
git clone https://github.com/alexzhu0/agent-runbook-kit.git
cd agent-runbook-kit
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m agent_runbook_kit examples/project.yaml
```

## Examples

```bash
PYTHONPATH=src python3 -m agent_runbook_kit examples/project.yaml
```

## API

The first release is CLI-first. Public Python APIs can be added after real usage proves the right shape.

## FAQ

**Does this call external AI APIs?**

No. The generated starter uses the Python standard library only.

**Is this production-ready?**

Treat `v0.1.0` as a focused utility release. Pin versions and review output before adding it to CI.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

## License

MIT
