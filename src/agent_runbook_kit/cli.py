"""Generate a minimal runbook kit for AI agent repositories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Sequence


def parse_simple_yaml(path: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def generate_runbook(path: str) -> str:
    data = parse_simple_yaml(path)
    name = data.get("name", "agent-project")
    audience = data.get("audience", "agent developers")
    demo = data.get("demo", "python3 -m tests")
    return f"""# {name} Runbook

## Audience

{audience}

## Release Gate

- README quickstart works.
- Tests pass.
- Eval fixture covers the main workflow.
- Launch copy names the user pain.

## Eval Checklist

- Happy path fixture.
- Failure fixture.
- Safety or boundary fixture.

## Demo

```bash
{demo}
```

## Launch Checklist

- Create `v0.1.0`.
- Add topics.
- Capture baseline metrics.
"""


def generate_documents(path: str) -> Dict[str, str]:
    data = parse_simple_yaml(path)
    name = data.get("name", "agent-project")
    demo = data.get("demo", "python3 -m tests")
    audience = data.get("audience", "agent developers")
    runbook = generate_runbook(path)
    readme = f"""# {name}

Small AI agent project for {audience}.

## Quickstart

```bash
{demo}
```

## Quality Gate

- Tests pass.
- Eval fixtures cover the primary workflow.
- Release notes explain the user-facing change.
"""
    eval_checklist = f"""# {name} Eval Checklist

- Happy path fixture proves the main demo.
- Failure fixture captures the most likely breakage.
- Safety fixture covers permissions, privacy, or irreversible actions.
- Regression command: `{demo}`
"""
    release_notes = f"""# {name} Release Notes

## User-facing change

- Describe the workflow improvement in one sentence.

## Verification

- `{demo}`
"""
    launch_checklist = f"""# {name} Launch Checklist

- README quickstart works from a fresh clone.
- GitHub topics match the target user.
- Social preview is set.
- Metrics snapshot captured after release.
"""
    return {
        "runbook": runbook,
        "README.md": readme,
        "eval-checklist.md": eval_checklist,
        "release-notes.md": release_notes,
        "launch-checklist.md": launch_checklist,
    }


def run(input_path: str, output_format: str = "text", kind: str = "runbook") -> str:
    documents = generate_documents(input_path)
    runbook = documents["runbook"]
    if output_format == "json":
        return json.dumps(documents, indent=2)
    if kind == "all":
        return "\n\n---\n\n".join(f"<!-- {name} -->\n{content}" for name, content in documents.items())
    return documents.get(kind, runbook)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a minimal runbook kit for AI agent repositories.")
    parser.add_argument("input", help="Project YAML")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--kind",
        choices=["runbook", "README.md", "eval-checklist.md", "release-notes.md", "launch-checklist.md", "all"],
        default="runbook",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format, args.kind))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
