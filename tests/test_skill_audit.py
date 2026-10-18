import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/nick-fury/scripts/audit.py"
SPEC = importlib.util.spec_from_file_location("skill_audit", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "example-skill"
        self.root.mkdir()

    def write(self, body, header="name: example-skill\ndescription: Una tarea concreta."):
        (self.root / "SKILL.md").write_text("---\n" + header + "\n---\n" + body)

    def test_reports_size_without_claiming_unmeasured_tokens(self):
        self.write("# Ejemplo\nHacer una tarea.")
        result = audit.audit(self.root)
        self.assertTrue(result["valid_required_fields"])
        self.assertIsNone(result["tokens"])
        self.assertEqual(result["encoding"], None)
        self.assertGreater(result["size"]["entry_bytes"], 0)

    def test_name_must_be_valid_and_match_folder(self):
        self.write("Pasos.", "name: Invalid--Name\ndescription: Algo.")
        result = audit.audit(self.root)
        self.assertFalse(result["valid_required_fields"])

    def test_local_references_must_exist_inside_skill(self):
        self.write("[Roto](references/missing.md)\n[Escape](../outside.md)")
        result = audit.audit(self.root)
        self.assertEqual(len(result["errors"]), 2)

    def test_budget_is_advisory_and_does_not_remove_necessary_rules(self):
        self.write("Una regla necesaria. " * 100)
        result = audit.audit(self.root)
        self.assertTrue(result["valid_required_fields"])
        self.assertTrue(result["warnings"])

    def test_duplicate_fields_are_rejected(self):
        self.write("Pasos.", "name: example-skill\ndescription: Uno.\ndescription: Dos.")
        self.assertFalse(audit.audit(self.root)["valid_required_fields"])

    def test_missing_tokenizer_does_not_fabricate_a_measurement(self):
        self.write("Una tarea.")
        with patch.dict("sys.modules", {"tiktoken": None}):
            result = audit.audit(self.root, encoding="o200k_base")
        self.assertIsNone(result["tokens"])
        self.assertTrue(result["measurement_error"])
