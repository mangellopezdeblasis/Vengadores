#!/usr/bin/env python3
"""Audit minimal skill fields, local links and size; token counting is optional."""
import argparse
import json
from pathlib import Path
import re
import sys


def scalar(raw):
    raw = raw.strip()
    if raw.startswith('"'):
        value = json.loads(raw)
    elif raw.startswith("'") and raw.endswith("'"):
        value = raw[1:-1].replace("''", "'")
    else:
        raw = raw.split(" #", 1)[0].strip()
        if raw.startswith("#"):
            raw = ""
        if not raw or raw[0] in "|>[{&*!" or ": " in raw:
            raise ValueError("Para YAML avanzado usar un validador completo; este auditor admite escalares simples.")
        if raw.lower() in {"true", "false", "null", "~"} or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", raw):
            raise ValueError("Los campos requeridos deben ser strings; entrecomillar valores ambiguos.")
        value = raw
    if not isinstance(value, str) or not value.strip():
        raise ValueError("El campo requerido debe ser texto no vacío.")
    return value


def audit(directory, encoding=None):
    root = Path(directory).resolve()
    result = {"skill": str(root), "validation_scope": "required_scalars_and_local_links",
              "errors": [], "warnings": [], "encoding": encoding, "tokens": None}
    try:
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", text, re.S)
        if not match:
            raise ValueError("Falta frontmatter delimitado por ---.")
        fields = {}
        for line in match[1].splitlines():
            item = re.match(r"^(name|description):[ \t]*(.*)$", line)
            if item:
                if item[1] in fields:
                    raise ValueError("Campo repetido: " + item[1])
                fields[item[1]] = scalar(item[2])
        name, description = fields.get("name", ""), fields.get("description", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            result["errors"].append("name no cumple el identificador requerido (1–64, minúsculas/números/guiones).")
        if name != root.name:
            result["errors"].append("name debe coincidir con la carpeta.")
        if not 1 <= len(description) <= 1024:
            result["errors"].append("description debe tener 1–1024 caracteres.")
        body = match[2].strip()
        if not body:
            result["errors"].append("El cuerpo está vacío.")
        for link in re.findall(r"\]\(([^)]+)\)", body):
            if re.match(r"https?://", link):
                continue
            target = link.split("#", 1)[0]
            if not target:
                continue
            path = (root / target).resolve()
            if not path.is_relative_to(root) or not path.exists():
                result["errors"].append("Referencia local ausente o externa a la skill: " + link)
        result["size"] = {"entry_bytes": len(text.encode("utf-8")),
                          "description_chars": len(description),
                          "body_words": len(body.split()), "body_lines": len(body.splitlines())}
        if len(description) > 240:
            result["warnings"].append("Descripción supera la meta local de 240 caracteres.")
        if len(body.split()) > 250 or len(body.splitlines()) > 45:
            result["warnings"].append("Núcleo supera la meta local de 250 palabras o 45 líneas; justificar o separar detalles.")
        if encoding:
            try:
                import tiktoken
                tokenizer = tiktoken.get_encoding(encoding)
                result["tokens"] = {"metadata_text": len(tokenizer.encode(name + "\n" + description)),
                                    "body": len(tokenizer.encode(body)),
                                    "entry": len(tokenizer.encode(text))}
                if result["tokens"]["body"] > 600:
                    result["warnings"].append("Cuerpo supera la meta local de 600 tokens en el encoding seleccionado.")
            except Exception as exc:
                result["measurement_error"] = type(exc).__name__ + ": " + str(exc)
        result["measurement_scope"] = "Solo texto del archivo; excluye referencias cargadas y envoltorios del host."
    except (OSError, ValueError) as exc:
        result["errors"].append(str(exc))
    result["valid_required_fields"] = not result["errors"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("--encoding", help="Encoding confirmado del modelo; requiere tiktoken instalado.")
    args = parser.parse_args(argv)
    result = audit(args.skill_directory, args.encoding)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["valid_required_fields"] and not result.get("measurement_error") else 2


if __name__ == "__main__":
    sys.exit(main())
