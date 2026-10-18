#!/usr/bin/env python3
"""Install Jarvis with its separate delegation skill; no network or agent execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1] / "skills" / "jarvis"
BUNDLED = SOURCE.parent / "delegacion-vengadores"
OPENCODE_AGENT = SOURCE.parents[1] / "integrations" / "opencode" / "jarvis.md"
HOST_DIRS = {"opencode": ".opencode/skills/jarvis", "codex": ".agents/skills/jarvis"}
BINDING = Path(".vengadores/jarvis.json")


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
    if not path.resolve().is_relative_to(project):
        raise ValueError("La configuración debe permanecer dentro del proyecto.")
    return path


def read_config(project):
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
        for name in ("contract.md", "roles.md", "flow.md", "delegation.md", "supervision.md"):
            if not (installed / "references" / name).is_file():
                raise ValueError("Instalación incompleta: falta references/" + name)
        dependency = data.get("delegation_skill")
        if not dependency:
            raise ValueError("Falta vincular la skill de delegación existente con bind.")
        dependency = delegation_file(dependency)
        if dependency.is_relative_to(installed.resolve()):
            raise ValueError("La skill de delegación debe estar separada de Jarvis.")
        if data.get("dependency_origin") == "bundled":
            for name in ("codex.md", "opencode.md"):
                if not (dependency.parent / "references" / name).is_file():
                    raise ValueError("Falta el adaptador de delegación: " + name)
        if data["host"] == "opencode" and not (project / ".opencode/agents/jarvis.md").is_file():
            raise ValueError("Falta el agente primario de Jarvis para OpenCode.")
        return {"state": "configurado", "host": data["host"],
                "skill": str(installed), "delegation_skill": str(dependency),
                "delegation_sha256": hashlib.sha256(dependency.read_bytes()).hexdigest(),
                "host_execution": "pendiente_de_invocacion_real"}
    except (ValueError, OSError, TypeError) as exc:
        return {"state": "bloqueado", "reason": str(exc),
                "host_execution": "no_verificado"}


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
            sub.add_argument("--replace", action="store_true",
                             help="Reemplaza explícitamente una instalación de Jarvis.")
    args = parser.parse_args(argv)
    try:
        project = Path(args.project).expanduser().resolve()
        if not project.is_dir():
            raise ValueError("El proyecto destino debe ser un directorio existente.")
        if args.action == "install":
            bundled = args.delegation_skill is None
            dependency = delegation_file(args.delegation_skill or BUNDLED)
            destination = project / HOST_DIRS[args.host]
            dependency_destination = destination.parent / "delegacion-vengadores"
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
            copies = [(SOURCE, destination)]
            if bundled:
                copies.append((BUNDLED, dependency_destination))
            if args.host == "opencode":
                if not OPENCODE_AGENT.is_file():
                    raise ValueError("No está el agente primario de OpenCode en la fuente.")
                copies.append((OPENCODE_AGENT, project / ".opencode/agents/jarvis.md"))
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
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
            if bundled:
                dependency = dependency_destination / "SKILL.md"
            write_config(project, {"schema_version": 1, "host": args.host,
                                  "skill_directory": HOST_DIRS[args.host],
                                  "delegation_skill": str(dependency),
                                  "dependency_origin": "bundled" if bundled else "external"})
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
