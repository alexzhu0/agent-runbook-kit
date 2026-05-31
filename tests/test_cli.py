import json
import tempfile
import unittest
from pathlib import Path

from agent_runbook_kit.cli import generate_runbook, run


class AgentRunbookKitTests(unittest.TestCase):
    def test_generates_named_runbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "project.yaml"
            path.write_text("name: demo-agent\naudience: builders\ndemo: make test\n", encoding="utf-8")
            runbook = generate_runbook(str(path))
        self.assertIn("# demo-agent Runbook", runbook)
        self.assertIn("make test", runbook)

    def test_json_output_contains_runbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "project.yaml"
            path.write_text("name: x\n", encoding="utf-8")
            payload = json.loads(run(str(path), "json"))
        self.assertIn("runbook", payload)


if __name__ == "__main__":
    unittest.main()
