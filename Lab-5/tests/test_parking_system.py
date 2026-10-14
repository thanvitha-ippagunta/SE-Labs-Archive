"""Regression tests for the campus parking permit manager."""

import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import parking_system as parking


class ParkingSystemTests(unittest.TestCase):
    """Test registration, validation, expiry, persistence and scanning."""

    def setUp(self):
        parking.permits.clear()

    def tearDown(self):
        parking.permits.clear()

    def test_registration_normalizes_and_records(self):
        records = []
        permit_id = parking.register_permit(" ka01ab1234 ", "a", records)
        self.assertTrue(permit_id.startswith("P"))
        self.assertEqual(len(permit_id), 6)
        self.assertEqual(records, [("KA01AB1234", "A")])
        self.assertEqual(parking.permits["KA01AB1234"]["zone"], "A")

    def test_reject_invalid_registration(self):
        for plate, zone in [("", "A"), (None, "A"), ("KA01AB1234", "Z")]:
            with self.subTest(plate=plate, zone=zone):
                self.assertIsNone(parking.register_permit(plate, zone))
        self.assertEqual(parking.permits, {})

    def test_zone_records_default_not_shared(self):
        records = []
        parking.register_permit("KA01AB1234", "A")
        parking.register_permit("KA02CD5678", "B", records)
        self.assertEqual(records, [("KA02CD5678", "B")])

    def test_no_duplicate_expiry_reset(self):
        original = parking.register_permit("KA01AB1234", "A")
        parking.set_expiry("KA01AB1234", "2020-01-01")
        duplicate = parking.register_permit("KA01AB1234", "B")
        self.assertEqual(duplicate, original)
        self.assertEqual(parking.permits["KA01AB1234"]["expiry"], "2020-01-01")
        self.assertEqual(parking.permits["KA01AB1234"]["zone"], "A")

    def test_expiry_today_is_valid(self):
        parking.register_permit("KA01AB1234", "A")
        parking.set_expiry("KA01AB1234", date.today().isoformat())
        self.assertFalse(parking.is_expired("KA01AB1234"))
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        parking.set_expiry("KA01AB1234", yesterday)
        self.assertTrue(parking.is_expired("KA01AB1234"))

    def test_bad_expiry_fails_closed(self):
        self.assertTrue(parking.is_expired("MISSING"))
        parking.register_permit("KA01AB1234", "A")
        parking.permits["KA01AB1234"]["expiry"] = "01/01/2020"
        self.assertTrue(parking.is_expired("KA01AB1234"))

    def test_revoke_existing_and_missing(self):
        self.assertFalse(parking.revoke_permit("UNKNOWN"))
        parking.register_permit("KA01AB1234", "A")
        self.assertTrue(parking.revoke_permit("ka01ab1234"))
        self.assertFalse(parking.revoke_permit("KA01AB1234"))

    def test_scan_flags_wrong_zone_or_missing(self):
        parking.register_permit("KA01AB1234", "A")
        parking.register_permit("KA05XY9999", "B")
        seen = ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]
        self.assertEqual(
            parking.scan_zone("A", seen), ["KA05XY9999", "TN09QQ1111"]
        )
        with self.assertRaises(ValueError):
            parking.scan_zone("Z", seen)

    def test_reject_bad_expiry_update(self):
        parking.register_permit("KA01AB1234", "A")
        with self.assertRaises(ValueError):
            parking.set_expiry("KA01AB1234", "01/01/2020")

    def test_database_round_trip(self):
        parking.register_permit("KA01AB1234", "A")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "permits.json"
            parking.save_permit_database(path)
            parking.permits.clear()
            parking.load_permit_database(path)
        self.assertIn("KA01AB1234", parking.permits)

    def test_invalid_records_not_restored(self):
        entries = {
            "": {"zone": "B", "permit": "P12345", "expiry": "2030-01-01"},
            "VALID": {"zone": "A", "permit": "P12346", "expiry": "2030-01-01"},
            "BAD": {"zone": "Z", "permit": "P12347", "expiry": "2030-01-01"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "permits.json"
            path.write_text(json.dumps(entries), encoding="utf-8")
            parking.load_permit_database(path)
        self.assertEqual(list(parking.permits), ["VALID"])

    def test_bad_json_keeps_existing_data(self):
        parking.register_permit("KA01AB1234", "A")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "permits.json"
            path.write_text("{invalid", encoding="utf-8")
            with self.assertRaises(ValueError):
                parking.load_permit_database(path)
        self.assertIn("KA01AB1234", parking.permits)

    def test_missing_database_clears_registry(self):
        parking.register_permit("KA01AB1234", "A")
        with tempfile.TemporaryDirectory() as directory:
            parking.load_permit_database(Path(directory) / "missing.json")
        self.assertEqual(parking.permits, {})


if __name__ == "__main__":
    unittest.main()
