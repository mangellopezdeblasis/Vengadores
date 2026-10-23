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
SPEC = importlib.util.spec_from_file_location('worker_guard', ROOT / 'skills/delegacion-vengadores/scripts/worker_guard.py')
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / 'project'
        self.project.mkdir()

    def run_guard(self, action, *args, project=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = guard.main([action, '--project', str(project or self.project), *args])
        return code, json.loads(output.getvalue())

    def prepare(self, task='one', role='thor', project=None):
        code, result = self.run_guard('prepare', '--role', role, '--task', task,
                                     '--version', 'baseline', '--context-ref', 'AGENTS.md', project=project)
        self.assertEqual(code, 0, result)
        self.assertEqual(result['state'], 'planificado')
        self.assertIsNone(result['worker_id'])
        return result['ticket']

    def bind(self, ticket, worker='/root/worker'):
        return self.run_guard('bind', '--ticket', ticket, '--worker-id', worker)

    def resume(self, ticket, role='thor', task='one', version='baseline'):
        return self.run_guard('resume', '--ticket', ticket, '--role', role,
                              '--task', task, '--version', version)

    def test_resume_only_linked_same_identity_and_context(self):
        ticket = self.prepare()
        self.assertEqual(self.resume(ticket)[0], 2)
        self.assertEqual(self.bind(ticket)[0], 0)
        code, result = self.resume(ticket)
        self.assertEqual(code, 0)
        self.assertEqual(result['worker_id'], '/root/worker')
        for options in ({'role': 'viuda'}, {'task': 'other'}, {'version': 'next'}):
            self.assertEqual(self.resume(ticket, **options)[0], 2)
        self.assertEqual(self.bind(ticket, '/root/replacement')[0], 2)
        self.assertFalse((self.project / 'root').exists())

    def test_distinct_tasks_require_distinct_worker_ids(self):
        one, two = self.prepare(), self.prepare('two')
        self.assertEqual(self.bind(one)[0], 0)
        self.assertEqual(self.bind(two)[0], 2)
        self.assertEqual(self.bind(two, '/root/another')[0], 0)
        self.assertEqual(self.resume(two, task='two')[1]['worker_id'], '/root/another')

    def test_reject_full_history_and_role_variants(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.run_guard('prepare', '--role', 'thor', '--task', 'x', '--version', 'v',
                           '--context-ref', 'AGENTS.md', '--fork-turns', 'all')
        for role in ('Thor', ' thor', '../thor', 'jarvis'):
            self.assertEqual(self.run_guard('prepare', '--role', role, '--task', 'x',
                                           '--version', 'v', '--context-ref', 'AGENTS.md')[0], 2)

    def test_symlink_escape_and_lock_reject_without_mutation(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        (self.project / '.vengadores').symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.run_guard('prepare', '--role', 'thor', '--task', 'x', '--version', 'v', '--context-ref', 'a')[0], 2)
        self.assertEqual(list(outside.iterdir()), [])
        (self.project / '.vengadores').unlink()
        ticket = self.prepare()
        state = self.project / '.vengadores/workers.json'
        original = state.read_bytes()
        (state.parent / 'workers.lock').touch()
        self.assertEqual(self.bind(ticket)[0], 2)
        self.assertEqual(state.read_bytes(), original)

    def test_corrupt_registry_is_blocked_without_overwrite(self):
        directory = self.project / '.vengadores'
        directory.mkdir()
        path = directory / 'workers.json'
        for contents in ('[]', '{', '{"schema_version": 1, "workers": {"x": []}}',
                         '{"schema_version": 1, "workers": {"x": {}}}'):
            path.write_text(contents)
            code, result = self.run_guard('prepare', '--role', 'thor', '--task', 'one',
                                          '--version', 'v', '--context-ref', 'AGENTS.md')
            self.assertEqual(code, 2, result)
            self.assertEqual(result['state'], 'bloqueado')
            self.assertEqual(path.read_text(), contents)
            self.assertFalse((directory / 'workers.lock').exists())

    def test_copied_workspace_and_changed_commit_rejected(self):
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True)
        subprocess.run(['git', '-C', str(self.project), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-qm', 'baseline'], check=True)
        ticket = self.prepare()
        self.bind(ticket)
        other = Path(self.tmp.name) / 'other'
        other.mkdir()
        shutil.copytree(self.project / '.vengadores', other / '.vengadores')
        self.assertEqual(self.run_guard('bind', '--ticket', ticket, '--worker-id', '/root/new', project=other)[0], 2)
        subprocess.run(['git', '-C', str(self.project), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '--allow-empty', '-qm', 'new'], check=True)
        self.assertEqual(self.resume(ticket)[0], 2)


if __name__ == '__main__':
    unittest.main()
