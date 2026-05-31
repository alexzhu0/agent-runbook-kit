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


def run(input_path: str, output_format: str = "text") -> str:
    runbook = generate_runbook(input_path)
    if output_format == "json":
        return json.dumps({"runbook": runbook}, indent=2)
    return runbook


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a minimal runbook kit for AI agent repositories.")
    parser.add_argument("input", help="Project YAML")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
