"""Short command for installing Vengadores into the current project."""
import argparse
from pathlib import Path

from . import configure_jarvis


def main(argv=None):
    parser = argparse.ArgumentParser(prog="vengadores")
    actions = parser.add_subparsers(dest="action", required=True)
    unidos = actions.add_parser("unidos", help="Instala Jarvis, delegación y Nick Fury en el proyecto actual.")
    unidos.add_argument("--project", default=str(Path.cwd()), help="Por defecto, directorio actual.")
    unidos.add_argument("--host", choices=configure_jarvis.HOST_DIRS, default="opencode")
    unidos.add_argument("--delegation-skill", help="Vincula una skill externa en lugar de la incluida.")
    unidos.add_argument("--replace", action="store_true", help="Reemplaza explícitamente la instalación.")
    unidos.add_argument("--activate", action="store_true", help="Activa Jarvis principal para Codex.")
    check = actions.add_parser("check", help="Comprueba instalación y activación efectiva.")
    check.add_argument("--project", default=str(Path.cwd()))
    args = parser.parse_args(argv)
    if args.action == "check":
        return configure_jarvis.main(["check", "--project", args.project])
    options = ["install", "--project", args.project, "--host", args.host]
    if args.delegation_skill:
        options.extend(["--delegation-skill", args.delegation_skill])
    if args.activate:
        options.append("--activate")
    if args.replace:
        options.append("--replace")
    return configure_jarvis.main(options)
