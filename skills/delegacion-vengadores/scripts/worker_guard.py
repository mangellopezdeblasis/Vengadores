#!/usr/bin/env python3
"""Local pre/post delegation guard. Does not spawn agents or restrict host permissions."""
import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
from contextlib import contextmanager


def project_root(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_dir():
        raise ValueError('El proyecto debe ser un directorio.')
    result = subprocess.run(['git', '-C', str(path), 'rev-parse', '--show-toplevel'],
                            capture_output=True, text=True)
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else path


def bounded(value):
    if not value.strip() or value != value.strip() or len(value) > 512 or any(ord(c) < 32 for c in value):
        raise ValueError('Identificador o referencia vacía, excesiva o con controles.')
    return value


def current_commit(project):
    result = subprocess.run(['git', '-C', str(project), 'rev-parse', 'HEAD'],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


@contextmanager
def registry(project):
    directory = project / '.vengadores'
    if directory.is_symlink() or not directory.resolve().is_relative_to(project):
        raise ValueError('.vengadores no puede escapar del proyecto ni ser symlink.')
    directory.mkdir(exist_ok=True)
    lock = directory / 'workers.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError('Registro ocupado: existe workers.lock; no se modificó estado.') from None
    try:
        os.close(descriptor)
        path = directory / 'workers.json'
        if path.is_symlink():
            raise ValueError('El registro no puede ser symlink.')
        data = json.loads(path.read_text()) if path.exists() else {'schema_version': 1, 'workers': {}}
        if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('workers'), dict):
            raise ValueError('Registro inválido.')
        identities = set()
        for ticket, entry in data['workers'].items():
            if (not isinstance(ticket, str) or not isinstance(entry, dict)
                    or any(not isinstance(entry.get(key), str) for key in ('role', 'task', 'workspace', 'version_ref'))
                    or entry.get('fork_turns') != 'none'
                    or not isinstance(entry.get('context_refs'), list)
                    or not entry['context_refs']
                    or any(not isinstance(ref, str) for ref in entry['context_refs'])
                    or entry.get('state') not in ('planificado', 'linked')
                    or (entry.get('git_commit') is not None and not isinstance(entry['git_commit'], str))):
                raise ValueError('Entrada corrupta en registro de workers.')
            identity = entry.get('worker_id')
            if ((entry['state'] == 'planificado' and identity is not None)
                    or (entry['state'] == 'linked' and (not isinstance(identity, str) or not identity))
                    or (identity is not None and identity in identities)):
                raise ValueError('Identidad corrupta en registro de workers.')
            if identity is not None:
                identities.add(identity)
        yield data
        fd, temporary = tempfile.mkstemp(dir=directory, prefix='.workers-', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w') as output:
                json.dump(data, output, indent=2, ensure_ascii=False)
                output.write('\n')
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    finally:
        lock.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    for action in ('prepare', 'bind', 'resume'):
        sub = actions.add_parser(action)
        sub.add_argument('--project', required=True)
        if action != 'prepare':
            sub.add_argument('--ticket', required=True)
        if action == 'bind':
            sub.add_argument('--worker-id', required=True)
        else:
            sub.add_argument('--role', required=True)
            sub.add_argument('--task', required=True)
            sub.add_argument('--version', required=True)
        if action == 'prepare':
            sub.add_argument('--context-ref', action='append', required=True)
            sub.add_argument('--fork-turns', choices=['none'], default='none')
    args = parser.parse_args(argv)
    try:
        project = project_root(args.project)
        with registry(project) as data:
            workers = data['workers']
            if args.action == 'prepare':
                role, task, version = map(bounded, (args.role, args.task, args.version))
                if not re.fullmatch(r'[a-z][a-z0-9-]*', role):
                    raise ValueError('El rol requiere identificador canónico ASCII en minúscula.')
                if role == 'jarvis':
                    raise ValueError('Jarvis principal no se registra como worker.')
                refs = list(dict.fromkeys(map(bounded, args.context_ref)))
                if len(refs) > 32:
                    raise ValueError('Demasiadas referencias; usar contexto mínimo.')
                for entry in workers.values():
                    if (entry['role'], entry['task'], entry['workspace'], entry['version_ref']) == (role, task, str(project), version):
                        raise ValueError('Encargo existente: usar su ticket para bind o resume.')
                ticket = str(uuid.uuid4())
                entry = {'role': role, 'task': task, 'workspace': str(project),
                         'version_ref': version, 'git_commit': current_commit(project), 'context_refs': refs, 'fork_turns': 'none',
                         'worker_id': None, 'state': 'planificado'}
                workers[ticket] = entry
            else:
                ticket = args.ticket
                if ticket not in workers:
                    raise ValueError('Ticket desconocido.')
                entry = workers[ticket]
                if entry['workspace'] != str(project):
                    raise ValueError('El ticket pertenece a otro workspace.')
                if entry.get('git_commit') != current_commit(project):
                    raise ValueError('Cambió HEAD del workspace: crear un encargo para la versión actual.')
                if args.action == 'bind':
                    worker = bounded(args.worker_id)
                    if entry['worker_id'] is not None:
                        raise ValueError('El ticket ya tiene identidad fija.')
                    if any(item['worker_id'] == worker for item in workers.values()):
                        raise ValueError('Worker ID ya asociado; no puede reutilizarse.')
                    entry.update(worker_id=worker, state='linked')
                else:
                    if (args.role, args.task, args.version) != (entry['role'], entry['task'], entry['version_ref']):
                        raise ValueError('Resume requiere el mismo rol, tarea y versión; crear worker nuevo.')
                    if entry['worker_id'] is None:
                        raise ValueError('Encargo planificado: falta bind con el ID real devuelto por el host.')
            result = dict(entry, ticket=ticket, host_execution='no_verificado')
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'state': 'bloqueado', 'reason': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    sys.exit(main())
