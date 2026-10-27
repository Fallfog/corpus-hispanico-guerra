"""Validación de la reserva editorial real, separada de pruebas sintéticas."""
import datetime as dt
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from editorial import validate, validate_monograph


class QueueQuality(unittest.TestCase):
    def test_reviewed_monographs(self):
        inventory = json.loads((ROOT / "editorial/inventory.json").read_text(encoding="utf-8"))
        used = {field: {x.get(field) for x in inventory} for field in ("id", "slug", "topic_key")}
        existing_ids = used["id"]
        seen = set()
        for path in sorted((ROOT / "content/cola").glob("*.json")):
            with self.subTest(path=path.name):
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn(record.get("status"), ("borrador", "revisado"))
                self.assertEqual(path.stem, record.get("id"))
                self.assertNotIn(record["id"], seen)
                seen.add(record["id"])
                for field in used:
                    self.assertNotIn(record[field], used[field], "Entrada o tema ya publicado")
                if record["status"] == "revisado":
                    ok, reason = validate(record)
                    self.assertTrue(ok, reason)
                    ok, reason = validate_monograph(record)
                    self.assertTrue(ok, reason)
                    dt.date.fromisoformat(record.get("not_before", ""))
                    for related_id in record.get("related", []):
                        self.assertIn(related_id, existing_ids, "Referencia relacionada inexistente")


if __name__ == "__main__":
    unittest.main()
