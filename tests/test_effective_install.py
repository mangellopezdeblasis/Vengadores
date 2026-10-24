import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('configure_effective', ROOT / 'scripts/configure_jarvis.py')
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class EffectiveInstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / 'project'
        self.project.mkdir()

    def cli(self, action, *options, project=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = installer.main([action, '--project', str(project or self.project), *options])
        return code, json.loads(output.getvalue())

    def install(self, *args, project=None):
        return self.cli('install', '--host', 'codex', '--activate', *args, project=project)

    def test_activation_preserves_text_and_replace_preserves_custom_config(self):
        agents = self.project / 'AGENTS.md'
        agents.write_bytes(b'Reglas locales existentes.\r\nSegunda regla.\r\n')
        code, result = self.install()
        self.assertEqual(code, 0, result)
        self.assertTrue(result['installed'])
        self.assertTrue(result['active'])
        first = agents.read_text()
        own_config = self.project / '.vengadores/config.yaml'
        generated = json.loads(own_config.read_text())
        self.assertEqual(generated['project']['repository'], str(self.project))
        self.assertIsNone(generated['project']['development_branch'])
        own_config.write_text('# config propia\nmaxparallel: 2\nchecks: null\n')
        own_config_before = own_config.read_bytes()
        config = self.project / '.vengadores/jarvis.json'
        data = json.loads(config.read_text())
        data.update(maxparallel=2, checks=None, custom={'keep': True})
        config.write_text(json.dumps(data))
        code, result = self.install('--replace')
        self.assertEqual(code, 0, result)
        self.assertEqual(agents.read_text(), first)
        self.assertEqual(own_config.read_bytes(), own_config_before)
        current = json.loads(config.read_text())
        for key in ('maxparallel', 'checks', 'custom'):
            self.assertEqual(current[key], data[key])
        self.assertTrue(current['author_skill'].startswith('.agents/'))
        self.assertTrue(agents.read_bytes().startswith(b'Reglas locales existentes.\r\nSegunda regla.\r\n'))
        self.assertEqual(first.count(installer.START), 1)

    def test_override_blocks_before_any_writes_and_invalidates_active(self):
        override = self.project / 'AGENTS.override.md'
        override.write_text('prioridad local')
        code, result = self.install()
        self.assertEqual(code, 2, result)
        self.assertEqual(list(self.project.iterdir()), [override])
        override.unlink()
        self.install()
        override.write_text('prioridad local')
        code, result = self.cli('check')
        self.assertEqual(code, 0, result)
        self.assertTrue(result['installed'])
        self.assertFalse(result['active'])

    def test_foreign_copied_binding_and_legacy_absolute_paths(self):
        self.install()
        config = self.project / '.vengadores/jarvis.json'
        data = json.loads(config.read_text())
        data.pop('project_root')
        for key in ('author_skill', 'escalation_skill', 'delegation_skill'):
            data[key] = str(self.project / data[key])
        config.write_text(json.dumps(data))
        self.assertEqual(self.cli('check')[0], 0)
        other = self.root / 'other'
        shutil.copytree(self.project, other)
        self.assertEqual(self.cli('check', project=other)[0], 2)
        self.assertEqual(self.install('--replace', project=other)[0], 0)
        self.assertTrue(self.cli('check', project=other)[1]['active'])

    def test_modern_foreign_binding_recovers_only_explicitly(self):
        self.install()
        other = self.root / 'modern-copy'
        shutil.copytree(self.project, other)
        self.assertEqual(self.cli('check', project=other)[0], 2)
        self.assertEqual(self.install(project=other)[0], 2)
        self.assertEqual(self.install('--replace', project=other)[0], 0)
        self.assertTrue(self.cli('check', project=other)[1]['active'])

    def test_real_git_worktree_and_nested_target_use_checkout_root(self):
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True)
        subprocess.run(['git', '-C', str(self.project), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-qm', 'baseline'], check=True)
        worktree = self.root / 'worktree'
        subprocess.run(['git', '-C', str(self.project), 'worktree', 'add', '-q', '-b', 'fixture', str(worktree)], check=True)
        self.assertTrue((worktree / '.git').is_file())
        nested = worktree / 'nested'
        nested.mkdir()
        code, result = self.install(project=nested)
        self.assertEqual(code, 0, result)
        self.assertTrue((worktree / 'AGENTS.md').is_file())
        self.assertFalse((nested / 'AGENTS.md').exists())
        self.assertFalse((self.project / '.agents').exists())
        cfg = json.loads((worktree / '.vengadores/config.yaml').read_text())
        self.assertEqual(cfg['project']['repository'], str(worktree))
        self.assertEqual(cfg['orchestrator']['entrypoint'], '.agents/skills/jarvis/SKILL.md')
        self.assertTrue(self.cli('check', project=nested)[1]['active'])

    def test_existing_external_dependency_survives_replace(self):
        dependency = self.root / 'external' / 'SKILL.md'
        dependency.parent.mkdir()
        dependency.write_text('---\nname: external\ndescription: Fixture.\n---\n')
        (dependency.parent / 'scripts').mkdir()
        shutil.copy2(ROOT / 'skills/delegacion-vengadores/scripts/worker_guard.py', dependency.parent / 'scripts/worker_guard.py')
        self.assertEqual(self.install('--delegation-skill', str(dependency))[0], 0)
        code, result = self.install('--replace')
        self.assertEqual(code, 0, result)
        self.assertEqual(result['delegation_skill'], str(dependency))
        self.assertIn(str(dependency.parent / 'scripts/worker_guard.py'), (self.project / 'AGENTS.md').read_text())

    def test_hulk_audit_resources_are_distributed_for_both_hosts(self):
        for host in ('codex', 'opencode'):
            with self.subTest(host=host):
                target = self.root / host
                target.mkdir()
                code, result = self.cli('install', '--host', host, project=target)
                self.assertEqual(code, 0, result)
                package = Path(result['subagents_directory']) / 'hulk/habilidades/auditoria-seguridad'
                self.assertTrue((package / 'SKILL.md').is_file())
                for name in ('SOURCE.json', 'upstream/LICENSE', 'upstream/report-schema.json',
                             'upstream/validate-findings.cjs', 'upstream/validate-coverage-ledger.cjs'):
                    self.assertEqual((package / name).read_bytes(),
                                     (ROOT / 'subagentes/hulk/habilidades/auditoria-seguridad' / name).read_bytes())
                (package / 'upstream/VALIDATION-AND-REPORTING.md').unlink()
                code, failure = self.cli('check', project=target)
                self.assertEqual(code, 2, failure)


if __name__ == '__main__':
    unittest.main()
