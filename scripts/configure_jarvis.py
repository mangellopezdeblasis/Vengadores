#!/usr/bin/env python3
"""Install Jarvis with its separate delegation skill; no network or agent execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import subprocess

SOURCE = Path(__file__).resolve().parents[1] / "skills" / "jarvis"
BUNDLED = SOURCE.parent / "delegacion-vengadores"
AUTHOR = SOURCE.parent / "nick-fury"
ESCALATION = SOURCE.parent / "escalacion-vengadores"
OPENCODE_AGENT = SOURCE.parents[1] / "integrations" / "opencode" / "jarvis.md"
OPENCODE_AUTHOR = OPENCODE_AGENT.with_name("nick-fury.md")
HOST_DIRS = {"opencode": ".opencode/skills/jarvis", "codex": ".agents/skills/jarvis"}
BINDING = Path(".vengadores/jarvis.json")
START = "<!-- vengadores:codex:start -->"
END = "<!-- vengadores:codex:end -->"


def project_root(value):
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise ValueError("El proyecto destino debe ser un directorio existente.")
    result = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True)
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else path


def reference(project, value):
    path = Path(value).expanduser()
    return (path if path.is_absolute() else project / path).resolve()


def local_reference(project, path):
    path = path.resolve()
    return str(path.relative_to(project)) if path.is_relative_to(project) else str(path)


def activation_text(guard=".agents/skills/delegacion-vengadores/scripts/worker_guard.py"):
    return START + "\n" + (
        "En la sesión principal, aplicar `.agents/skills/jarvis/SKILL.md` como Jarvis.\n"
        "Jarvis decide los roles y Thor ejecuta. Los workers mantienen su rol y tarea y no redelegan.\n"
        f"Antes de un worker Codex nuevo usar el guard de `{guard}`: "
        "prepare con contexto mínimo y fork_turns none, luego bind con el ID real.\n"
        "Para continuidad validar resume del mismo rol, tarea, workspace y versión.\n"
        "El guard no limita llamadas manuales ni permisos del host.\n"
    ) + END


def activation_content(project, guard):
    if (project / "AGENTS.override.md").exists():
        raise ValueError("AGENTS.override.md tiene prioridad: activación bloqueada antes de escribir; integrar allí explícitamente.")
    path = project / "AGENTS.md"
    if path.is_symlink():
        raise ValueError("AGENTS.md no puede ser symlink para activación.")
    text = path.read_bytes().decode("utf-8") if path.exists() else ""
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError("Bloque administrado ambiguo en AGENTS.md.")
    if START in text:
        if text.index(END) < text.index(START):
            raise ValueError("Bloque administrado inválido.")
        return text[:text.index(START)] + activation_text(guard) + text[text.index(END) + len(END):]
    return text + ("\n\n" if text and not text.endswith("\n\n") else "") + activation_text(guard) + "\n"


def active(project, data):
    dependency = reference(project, data["delegation_skill"])
    guard = dependency.parent / "scripts/worker_guard.py"
    path = project / "AGENTS.md"
    return (not (project / "AGENTS.override.md").exists() and not path.is_symlink()
            and path.is_file() and path.read_bytes().decode("utf-8").count(START) == 1
            and guard.is_file()
            and (project / ".vengadores/config.yaml").is_file()
            and not (project / ".vengadores/config.yaml").is_symlink()
            and activation_text(local_reference(project, guard)) in path.read_bytes().decode("utf-8"))



def skill_file(value):
    path = Path(value).expanduser().resolve()
    if path.is_dir():
        path = path / "SKILL.md"
    if path.name != "SKILL.md" or not path.is_file():
        raise ValueError("La dependencia debe apuntar a un SKILL.md existente.")
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match or any(not re.search(rf"^{key}:[ \t]*\S", match[1], re.M)
                        for key in ("name", "description")):
        raise ValueError("SKILL.md requiere frontmatter con name y description.")
    return path


def delegation_file(value):
    path = skill_file(value)
    name = re.search(r"^name:[ \t]*([^\n]+)", path.read_text(encoding="utf-8"), re.M)[1]
    if name.strip().strip("\"'").lower() == "jarvis":
        raise ValueError("Jarvis no puede delegarse a sí mismo como dependencia.")
    return path


def config_path(project):
    path = project / BINDING
    if (project / ".vengadores").is_symlink() or not path.resolve().is_relative_to(project):
        raise ValueError("La configuración debe permanecer dentro del proyecto.")
    return path


def read_config(project, allow_foreign=False):
    path = config_path(project)
    if not path.is_file():
        raise ValueError("Jarvis no está instalado: falta .vengadores/jarvis.json.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("La configuración debe ser un objeto JSON.")
    if data.get("schema_version") != 1 or data.get("host") not in HOST_DIRS:
        raise ValueError("Versión o host de configuración no soportados.")
    if data.get("skill_directory") != HOST_DIRS[data["host"]]:
        raise ValueError("La ruta instalada no corresponde al host declarado.")
    if not allow_foreign and data.get("project_root") and reference(project, data["project_root"]) != project:
        raise ValueError("El vínculo pertenece a otro checkout; reinstalar explícitamente.")
    return data


def write_config(project, data):
    path = config_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check(project):
    try:
        data = read_config(project)
        installed = project / data["skill_directory"]
        if not installed.resolve().is_relative_to(project):
            raise ValueError("La skill instalada debe permanecer dentro del proyecto.")
        skill_file(installed)
        for name in ("contract.md", "roles.md", "flow.md", "delegation.md", "supervision.md", "orchestration.md"):
            if not (installed / "references" / name).is_file():
                raise ValueError("Instalación incompleta: falta references/" + name)
        dependency = data.get("delegation_skill")
        if not dependency:
            raise ValueError("Falta vincular la skill de delegación existente con bind.")
        dependency = delegation_file(reference(project, dependency))
        if dependency.is_relative_to(installed.resolve()):
            raise ValueError("La skill de delegación debe estar separada de Jarvis.")
        if data.get("dependency_origin") == "bundled":
            for name in ("codex.md", "opencode.md", "protocol.md"):
                if not (dependency.parent / "references" / name).is_file():
                    raise ValueError("Falta el adaptador de delegación: " + name)
            expected_dependency = installed.parent / "delegacion-vengadores" / "SKILL.md"
            if dependency != expected_dependency.resolve():
                raise ValueError("Delegación bundled apunta a otro checkout.")
            if not (dependency.parent / "scripts/worker_guard.py").is_file():
                raise ValueError("Falta el guard de identidad de delegación.")
        if data["host"] == "opencode" and not (project / ".opencode/agents/jarvis.md").is_file():
            raise ValueError("Falta el agente primario de Jarvis para OpenCode.")
        author = installed.parent / "nick-fury" / "SKILL.md"
        if not data.get("author_skill") or reference(project, data["author_skill"]) != author.resolve():
            raise ValueError("Falta vincular Nick Fury; reinstalar con --replace.")
        if not author.resolve().is_relative_to(project):
            raise ValueError("Nick Fury debe permanecer dentro del proyecto.")
        skill_file(author)
        for name in ("references/authoring.md", "references/tokens.md", "scripts/audit.py",
                     "assets/skill.md", "assets/opencode-agent.md", "assets/task.json"):
            if not (author.parent / name).is_file():
                raise ValueError("Nick Fury incompleto: falta " + name)
        if data["host"] == "opencode" and not (project / ".opencode/agents/nick-fury.md").is_file():
            raise ValueError("Falta el subagente Nick Fury para OpenCode.")
        escalation = installed.parent / "escalacion-vengadores" / "SKILL.md"
        if not data.get("escalation_skill") or reference(project, data["escalation_skill"]) != escalation.resolve():
            raise ValueError("Falta vincular escalada; reinstalar con --replace.")
        if not escalation.resolve().is_relative_to(project):
            raise ValueError("La skill de escalada debe permanecer dentro del proyecto.")
        skill_file(escalation)
        for name in ("policy.md", "profiles.json"):
            if not (escalation.parent / "references" / name).is_file():
                raise ValueError("Escalada incompleta: falta " + name)
        profiles = json.loads((escalation.parent / "references/profiles.json").read_text())
        if (not isinstance(profiles, dict) or profiles.get("schema_version") != 1
                or not isinstance(profiles.get("roles"), dict) or not profiles["roles"]):
            raise ValueError("Perfiles de escalada inválidos.")
        for role, profile in profiles["roles"].items():
            if (not isinstance(role, str) or not isinstance(profile, dict)
                    or profile.get("nivel") not in ("basico", "estandar", "avanzado")
                    or profile.get("esfuerzo") not in ("bajo", "medio", "alto")):
                raise ValueError("Perfil de escalada inválido: " + str(role))
        return {"state": "configurado", "installed": True,
                "active": active(project, data) if data["host"] == "codex" else None,
                "activation": "active" if data["host"] == "codex" and active(project, data) else "not_active",
                "session_startup": "pendiente_de_sesion_nueva",
                "host": data["host"],
                "skill": str(installed), "delegation_skill": str(dependency),
                "delegation_sha256": hashlib.sha256(dependency.read_bytes()).hexdigest(),
                "author_skill": str(author),
                "escalation_skill": str(escalation),
                "host_execution": "pendiente_de_invocacion_real"}
    except (ValueError, OSError, TypeError) as exc:
        return {"state": "bloqueado", "reason": str(exc),
                "host_execution": "no_verificado"}


def minimal_config(project, destination):
    source_root = SOURCE.parents[1]
    revision = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
    changed = subprocess.run(["git", "-C", str(source_root), "status", "--porcelain"],
                             capture_output=True, text=True)
    data = {
        "schema_version": 1,
        "project": {"id": project.name, "repository": str(project), "development_branch": None},
        "vengadores": {"repository": str(source_root),
                       "revision": revision.stdout.strip() if revision.returncode == 0 else None,
                       "local_modifications": bool(changed.stdout) if changed.returncode == 0 else None},
        "orchestrator": {"name": "Jarvis", "kind": "skill", "authoring_role": "Nick Fury",
                         "entrypoint": str((destination / "SKILL.md").relative_to(project)),
                         "delegation_binding": str(BINDING)},
        "context": {"project_rules": ["AGENTS.md"], "memory_sources": [], "load_by_relevance": True},
        "artifacts": {"task_directory": ".vengadores/tasks"},
        "checks": {"build_command": None, "test_command": None, "e2e_candidate_command": None,
                   "e2e_dev_command": None},
        "delivery": {"deploy_dev_command": None, "recovery_policy": None},
    }
    # JSON is a YAML 1.2 subset; quote every scalar to avoid project-name coercion.
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for action in ("install", "bind", "check"):
        sub = commands.add_parser(action)
        sub.add_argument("--project", required=True)
        if action != "check":
            sub.add_argument("--delegation-skill", required=action == "bind")
        if action == "install":
            sub.add_argument("--host", choices=HOST_DIRS, default="opencode")
            sub.add_argument("--activate", action="store_true", help="Activa Jarvis principal en AGENTS.md para Codex.")
            sub.add_argument("--replace", action="store_true",
                             help="Reemplaza explícitamente las skills distribuidas de Vengadores.")
    args = parser.parse_args(argv)
    try:
        project = project_root(args.project)
        if not project.is_dir():
            raise ValueError("El proyecto destino debe ser un directorio existente.")
        if args.action == "install":
            if args.activate and args.host != "codex":
                raise ValueError("--activate requiere --host codex.")
            existing = read_config(project, allow_foreign=args.replace) if config_path(project).exists() else {}
            chosen_dependency = args.delegation_skill
            if chosen_dependency is None and existing.get("dependency_origin") == "external":
                chosen_dependency = str(reference(project, existing["delegation_skill"]))
            bundled = chosen_dependency is None
            dependency = delegation_file(chosen_dependency or BUNDLED)
            destination = project / HOST_DIRS[args.host]
            dependency_destination = destination.parent / "delegacion-vengadores"
            activation = None
            if args.activate:
                guard_source = dependency.parent / "scripts/worker_guard.py"
                if not guard_source.is_file():
                    raise ValueError("La dependencia externa no distribuye scripts/worker_guard.py; no se puede activar el guard.")
                guard_target = (dependency_destination / "scripts/worker_guard.py") if bundled else guard_source
                activation = activation_content(project, local_reference(project, guard_target))
                own_config = project / ".vengadores/config.yaml"
                if own_config.is_symlink():
                    raise ValueError("config.yaml no puede ser symlink para activación.")
                if own_config.exists() and not own_config.is_file():
                    raise ValueError("config.yaml debe ser un archivo.")
            config_path(project)  # Validate before modifying either location.
            if not destination.resolve().is_relative_to(project):
                raise ValueError("La instalación debe permanecer dentro del proyecto.")
            if dependency and dependency.is_relative_to(destination.resolve()):
                raise ValueError("La skill de delegación debe estar separada de Jarvis.")
            if SOURCE.resolve().is_relative_to(destination.resolve()) or destination.resolve().is_relative_to(SOURCE.resolve()):
                raise ValueError("El destino no puede superponerse con la fuente de Jarvis.")
            if destination.is_symlink():
                raise ValueError("El destino de instalación no puede ser un symlink.")
            if destination.exists() and not args.replace:
                raise ValueError("Jarvis ya existe; usar --replace para reemplazarlo.")
            if config_path(project).exists() and not args.replace:
                raise ValueError("El proyecto ya tiene un vínculo; usar bind o --replace.")
            skill_file(SOURCE)
            skill_file(AUTHOR)
            skill_file(ESCALATION)
            author_destination = destination.parent / "nick-fury"
            copies = [(SOURCE, destination), (AUTHOR, author_destination),
                      (ESCALATION, destination.parent / "escalacion-vengadores")]
            if bundled:
                copies.append((BUNDLED, dependency_destination))
            if args.host == "opencode":
                if not OPENCODE_AGENT.is_file() or not OPENCODE_AUTHOR.is_file():
                    raise ValueError("Falta un perfil de agente de OpenCode en la fuente.")
                copies.append((OPENCODE_AGENT, project / ".opencode/agents/jarvis.md"))
                copies.append((OPENCODE_AUTHOR, project / ".opencode/agents/nick-fury.md"))
            # Validate every target before replacing any installation.
            for source, target in copies:
                if not target.resolve().is_relative_to(project) or target.is_symlink():
                    raise ValueError("El destino no puede ser externo ni un symlink.")
                if (source.resolve().is_relative_to(target.resolve()) or
                        target.resolve().is_relative_to(source.resolve())):
                    raise ValueError("El destino no puede superponerse con la fuente.")
                if target.exists() and not args.replace:
                    raise ValueError("Existe una skill o agente del destino; usar --replace.")
            for source, target in copies:
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                else:
                    shutil.copy2(source, target)
            if bundled:
                dependency = dependency_destination / "SKILL.md"
            data = dict(existing)
            data.update({"schema_version": 1, "host": args.host,
                                  "skill_directory": HOST_DIRS[args.host],
                                  "project_root": str(project),
                                  "delegation_skill": local_reference(project, dependency),
                                  "author_skill": local_reference(project, author_destination / "SKILL.md"),
                                  "escalation_skill": local_reference(project, destination.parent / "escalacion-vengadores" / "SKILL.md"),
                                  "dependency_origin": "bundled" if bundled else "external"})
            write_config(project, data)
            if activation is not None:
                own_config = project / ".vengadores/config.yaml"
                if not own_config.exists():
                    own_config.write_text(minimal_config(project, destination))
                (project / "AGENTS.md").write_bytes(activation.encode("utf-8"))
            result = check(project)
            result["installed"] = True
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0 if result["state"] == "configurado" else 2
        if args.action == "bind":
            data = read_config(project)
            dependency = delegation_file(args.delegation_skill)
            if dependency.is_relative_to((project / data["skill_directory"]).resolve()):
                raise ValueError("La skill de delegación debe estar separada de Jarvis.")
            data["delegation_skill"] = str(dependency)
            data["dependency_origin"] = "external"
            write_config(project, data)
        result = check(project)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["state"] == "configurado" else 2
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({"state": "bloqueado", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
