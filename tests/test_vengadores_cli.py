import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommandTests(unittest.TestCase):
    def run_command(self, project, *options):
        env = dict(os.environ, PATH=str(ROOT) + os.pathsep + os.environ.get("PATH", ""))
        return subprocess.run(["vengadores", "unidos", *options], cwd=project,
                              env=env, capture_output=True, text=True)

    def test_short_command_targets_current_directory_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="proyecto con espacios ") as project:
            result = self.run_command(project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["host"], "opencode")
            self.assertEqual(data["state"], "configurado")
            self.assertTrue((Path(project) / ".opencode/skills/jarvis/SKILL.md").is_file())
            self.assertTrue((Path(project) / ".opencode/skills/delegacion-vengadores/SKILL.md").is_file())
            self.assertTrue((Path(project) / ".opencode/skills/nick-fury/SKILL.md").is_file())

    def test_optional_host_codex_is_forwarded(self):
        with tempfile.TemporaryDirectory() as project:
            result = self.run_command(project, "--host", "codex")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((Path(project) / ".agents/skills/jarvis/SKILL.md").is_file())

    def test_host_claude_installs_agents_and_activation(self):
        with tempfile.TemporaryDirectory() as project:
            root = Path(project)
            (root / "CLAUDE.md").write_text("Reglas propias.\n")
            result = self.run_command(project, "--host", "claude", "--activate")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["host"], "claude")
            self.assertTrue(data["active"])
            self.assertTrue((root / ".agents/skills/jarvis/SKILL.md").is_file())
            self.assertTrue((root / ".agents/skills/delegacion-vengadores/references/claude.md").is_file())
            self.assertTrue((root / ".agents/subagentes/thor/SKILL.md").is_file())
            self.assertEqual(sorted(p.name for p in (root / ".claude").iterdir()), ["agents"])
            agent = (root / ".claude/agents/thor.md").read_text()
            self.assertIn("name: thor", agent)
            self.assertIn(".agents/subagentes/thor/SKILL.md", agent)
            self.assertNotIn("{", agent)
            self.assertEqual(len(list((root / ".claude/agents").glob("*.md"))), 11)
            claude_md = (root / "CLAUDE.md").read_text()
            self.assertTrue(claude_md.startswith("Reglas propias.\n"))
            self.assertIn(".agents/skills/jarvis/SKILL.md", claude_md)
            again = self.run_command(project, "--host", "claude", "--activate", "--replace")
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertEqual((root / "CLAUDE.md").read_text(), claude_md)
            (root / ".claude/agents/hulk.md").unlink()
            env = dict(os.environ, PATH=str(ROOT) + os.pathsep + os.environ.get("PATH", ""))
            check = subprocess.run(["vengadores", "check"], cwd=project, env=env,
                                   capture_output=True, text=True)
            self.assertEqual(check.returncode, 2)
            self.assertIn("hulk", json.loads(check.stdout)["reason"])

    def test_short_command_preserves_existing_skill(self):
        with tempfile.TemporaryDirectory() as project:
            target = Path(project) / ".opencode/skills/jarvis/SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text("trabajo existente")
            result = self.run_command(project)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_text(), "trabajo existente")


if __name__ == "__main__":
    unittest.main()
