import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DATE_FIELDS = {
    "informal_status": "open",
    "formal_status": "Lean",
    "status": "open",
    "formalized": "yes",
}


class ValidateDatesTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "schema", "data"):
            (self.root / directory).mkdir()
        for name in ("scripts/validate.py", "scripts/derive_status.py",
                     "schema/problems.schema.json"):
            shutil.copyfile(ROOT / name, self.root / name)

    def validate_rows(self, rows):
        # JSON is valid YAML, and keeps date fixtures as quoted strings.
        (self.root / "data/problems.yaml").write_text(
            json.dumps(rows), encoding="utf-8"
        )
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/validate.py")],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )

    def test_rejects_invalid_dates_in_every_status_field(self):
        cases = [
            (field, state, date)
            for field, state in DATE_FIELDS.items()
            for date in ("2026-02-32", "2025-12-2", "2025-02-29")
        ]
        result = self.validate_rows([
            {"number": str(i + 1), field: {"state": state, "last_update": date}}
            for i, (field, state, date) in enumerate(cases)
        ])
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        for i, (field, _, date) in enumerate(cases):
            with self.subTest(field=field, date=date):
                self.assertIn(
                    f"[schema] at '{i}/{field}/last_update': "
                    f"'{date}' is not a 'date'", result.stdout,
                )

    def test_accepts_valid_dates_and_omitted_optional_fields(self):
        rows = [
            {"number": str(i + 1), field: {"state": state, "last_update": date}}
            for i, (field, state, date) in enumerate(
                (field, state, date)
                for field, state in DATE_FIELDS.items()
                for date in ("2024-02-29", "2026-02-02")
            )
        ]
        rows.append({"number": "9"})
        result = self.validate_rows(rows)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation OK.", result.stdout)


if __name__ == "__main__":
    unittest.main()
