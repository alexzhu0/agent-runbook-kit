import json
import tempfile
import unittest
from pathlib import Path

from agent_runbook_kit.cli import generate_documents, generate_runbook, run


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
        self.assertIn("eval-checklist.md", payload)

    def test_generates_all_expected_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "project.yaml"
            path.write_text("name: demo-agent\naudience: builders\ndemo: make test\n", encoding="utf-8")

            docs = generate_documents(str(path))

        self.assertIn("README.md", docs)
        self.assertIn("release-notes.md", docs)
        self.assertIn("Launch Checklist", docs["launch-checklist.md"])

    def test_kind_selects_single_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "project.yaml"
            path.write_text("name: demo-agent\n", encoding="utf-8")

            output = run(str(path), kind="eval-checklist.md")

        self.assertIn("Eval Checklist", output)


if __name__ == "__main__":
    unittest.main()
