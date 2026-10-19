import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "configure_jarvis.py"
SPEC = importlib.util.spec_from_file_location("configure_jarvis", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.dependency = self.root / "delegation" / "SKILL.md"
        self.dependency.parent.mkdir()
        self.dependency.write_text("---\nname: fixture-delegation\ndescription: Test fixture only.\n---\n")

    def run_cli(self, action, *extra):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = module.main([action, "--project", str(self.project), *extra])
        return code, json.loads(output.getvalue())

    def test_default_install_includes_separate_dependency_and_can_bind_external(self):
        code, result = self.run_cli("install")
        self.assertEqual(code, 0)
        self.assertTrue(result["installed"])
        self.assertEqual(result["state"], "configurado")
        self.assertEqual(self.run_cli("check")[0], 0)
        self.assertEqual(Path(result["delegation_skill"]).parent.name, "delegacion-vengadores")
        self.assertTrue((self.project / ".opencode/agents/jarvis.md").is_file())
        self.assertTrue((self.project / ".opencode/agents/nick-fury.md").is_file())
        self.assertTrue(Path(result["author_skill"]).is_file())
        code, result = self.run_cli("bind", "--delegation-skill", str(self.dependency))
        self.assertEqual(code, 0)
        self.assertEqual(result["state"], "configurado")
        self.assertEqual(result["host_execution"], "pendiente_de_invocacion_real")

    def test_codex_install_contains_local_references_without_copying_dependency(self):
        code, result = self.run_cli("install", "--host", "codex", "--delegation-skill", str(self.dependency))
        self.assertEqual(code, 0)
        installed = Path(result["skill"])
        self.assertEqual(installed, self.project / ".agents/skills/jarvis")
        self.assertTrue((installed / "references/flow.md").is_file())
        self.assertEqual(Path(result["delegation_skill"]), self.dependency)
        self.assertFalse((installed / "delegation/SKILL.md").exists())

    def test_invalid_dependency_does_not_modify_project(self):
        code, _ = self.run_cli("install", "--delegation-skill", str(self.root / "missing"))
        self.assertEqual(code, 2)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_existing_skill_is_not_overwritten_without_replace(self):
        self.run_cli("install")
        installed = self.project / ".opencode/skills/jarvis/SKILL.md"
        installed.write_text("custom work")
        code, _ = self.run_cli("install")
        self.assertEqual(code, 2)
        self.assertEqual(installed.read_text(), "custom work")

    def test_dependency_disappearing_is_not_reported_as_ready(self):
        self.run_cli("install", "--delegation-skill", str(self.dependency))
        self.dependency.unlink()
        code, result = self.run_cli("check")
        self.assertEqual(code, 2)
        self.assertEqual(result["state"], "bloqueado")

    def test_jarvis_cannot_bind_itself(self):
        self.run_cli("install")
        code, _ = self.run_cli("bind", "--delegation-skill", str(module.SOURCE / "SKILL.md"))
        self.assertEqual(code, 2)

    def test_missing_binding_is_not_reported_as_ready(self):
        self.run_cli("install")
        config = self.project / ".vengadores/jarvis.json"
        data = json.loads(config.read_text())
        data["delegation_skill"] = None
        config.write_text(json.dumps(data))
        code, result = self.run_cli("check")
        self.assertEqual(code, 2)
        self.assertEqual(result["state"], "bloqueado")

    def test_missing_supervisor_contract_blocks_incomplete_installation(self):
        self.run_cli("install")
        reference = self.project / ".opencode/skills/jarvis/references/supervision.md"
        reference.unlink()
        code, result = self.run_cli("check")
        self.assertEqual(code, 2)
        self.assertIn("supervision.md", result["reason"])

    def test_conflicting_agent_is_preserved_before_installation(self):
        agent = self.project / ".opencode/agents/jarvis.md"
        agent.parent.mkdir(parents=True)
        agent.write_text("existing agent")
        code, _ = self.run_cli("install")
        self.assertEqual(code, 2)
        self.assertEqual(agent.read_text(), "existing agent")
        self.assertFalse((self.project / ".opencode/skills/jarvis").exists())

    def test_missing_author_resources_block_incomplete_installation(self):
        self.run_cli("install")
        (self.project / ".opencode/skills/nick-fury/scripts/audit.py").unlink()
        code, result = self.run_cli("check")
        self.assertEqual(code, 2)
        self.assertIn("Nick Fury incompleto", result["reason"])

    def test_existing_nick_fury_is_preserved_before_other_files_are_written(self):
        author = self.project / ".opencode/agents/nick-fury.md"
        author.parent.mkdir(parents=True)
        author.write_text("existing author")
        code, _ = self.run_cli("install")
        self.assertEqual(code, 2)
        self.assertEqual(author.read_text(), "existing author")
        self.assertFalse((self.project / ".opencode/skills/jarvis").exists())


    def test_escalation_is_installed_for_both_hosts_and_missing_policy_blocks(self):
        for host in ("codex", "opencode"):
            with self.subTest(host=host):
                code, result = self.run_cli("install", "--host", host, "--replace")
                self.assertEqual(code, 0, result)
                escalation = Path(result["escalation_skill"])
                self.assertEqual(escalation.parent.name, "escalacion-vengadores")
                profiles = json.loads((escalation.parent / "references/profiles.json").read_text())
                self.assertEqual(profiles["schema_version"], 1)
                self.assertTrue(profiles["roles"])
                (escalation.parent / "references/policy.md").unlink()
                code, failure = self.run_cli("check")
                self.assertEqual(code, 2)
                self.assertIn("policy.md", failure["reason"])

    def test_existing_escalation_preserved_before_any_installation_writes(self):
        escalation = self.project / ".opencode/skills/escalacion-vengadores/SKILL.md"
        escalation.parent.mkdir(parents=True)
        escalation.write_text("custom escalation")
        code, _ = self.run_cli("install")
        self.assertEqual(code, 2)
        self.assertEqual(escalation.read_text(), "custom escalation")
        self.assertFalse((self.project / ".opencode/skills/jarvis").exists())

    def test_invalid_portable_profile_is_not_reported_ready(self):
        code, result = self.run_cli("install")
        self.assertEqual(code, 0, result)
        profiles = Path(result["escalation_skill"]).parent / "references/profiles.json"
        profiles.write_text(json.dumps({"schema_version": 1, "roles": {
            "thor": {"nivel": "modelo-inventado", "esfuerzo": "medio"}}}))
        code, result = self.run_cli("check")
        self.assertEqual(code, 2)
        self.assertIn("Perfil de escalada inválido", result["reason"])


if __name__ == "__main__":
    unittest.main()
