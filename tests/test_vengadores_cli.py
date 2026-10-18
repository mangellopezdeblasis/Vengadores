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
