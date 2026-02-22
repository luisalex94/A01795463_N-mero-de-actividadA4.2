"""Unit tests for main.py helpers: one positive and one negative test per method.

These tests call the helper functions directly and capture stdout where
appropriate. Temporary files are used for JSON input and storage isolation.
"""
from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


class MainHelpersTests(unittest.TestCase):
    """Positive and negative tests for each helper in main.py."""

    def setUp(self) -> None:
        # Make local package importable
        import sys

        project_dir = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(project_dir))

        # Import after sys.path adjusted
        from src import main as cli_main
        from src.storage import Storage
        from src.models import Hotel, Customer, Reservation

        self.cli = cli_main
        self.Storage = Storage
        self.Hotel = Hotel
        self.Customer = Customer
        self.Reservation = Reservation

        self.tmpdir = tempfile.TemporaryDirectory()
        base = Path(self.tmpdir.name)
        self.hotels = str(base / "hotels.json")
        self.customers = str(base / "customers.json")
        self.reservations = str(base / "reservations.json")

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _write(self, path: str, obj) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)

    # _detect_files
    def test_detect_files_positive_keyword(self) -> None:
        mapping = self.cli._detect_files([
            "/tmp/x_hotels.json",
            "/tmp/x_customers.json",
            "/tmp/x_reservations.json",
        ])
        self.assertIn("hotels", mapping)
        self.assertIn("customers", mapping)

    def test_detect_files_negative_not_enough(self) -> None:
        with self.assertRaises(SystemExit):
            self.cli._detect_files(["only_one.json"])

    # _create_hotel_from_file
    def test_create_hotel_from_file_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        hpath = Path(self.tmpdir.name) / "h.json"
        self._write(str(hpath), {"hotel_id": 1, "name": "H1", "address": "A", "rooms": {}})
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._create_hotel_from_file(str(hpath), store)
        self.assertIn("Hotel created", f.getvalue())

    def test_create_hotel_from_file_negative_bad_json(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        bad = Path(self.tmpdir.name) / "bad_h.json"
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{ not json }")
        with self.assertRaises(SystemExit) as cm:
            self.cli._create_hotel_from_file(str(bad), store)
        self.assertEqual(cm.exception.code, 2)

    # _create_customer_from_file
    def test_create_customer_from_file_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        cpath = Path(self.tmpdir.name) / "c.json"
        self._write(str(cpath), {"customer_id": 2, "name": "C2", "email": "e", "phone": "p"})
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._create_customer_from_file(str(cpath), store)
        self.assertIn("Customer created", f.getvalue())

    def test_create_customer_from_file_negative_bad_json(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        bad = Path(self.tmpdir.name) / "bad_c.json"
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{ invalid }")
        with self.assertRaises(SystemExit) as cm:
            self.cli._create_customer_from_file(str(bad), store)
        self.assertEqual(cm.exception.code, 2)

    # _create_reservation_from_file
    def test_create_reservation_from_file_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        # prepare customer and hotel
        store.create_hotel(self.Hotel.from_dict({"hotel_id": 3, "name": "H3", "address": "A", "rooms": {"1": 1}}))
        store.create_customer(self.Customer.from_dict({"customer_id": 4, "name": "C4", "email": "e", "phone": "p"}))
        rpath = Path(self.tmpdir.name) / "r.json"
        self._write(str(rpath), {"reservation_id": 5, "customer_id": 4, "hotel_id": 3, "room_number": "1", "start_date": "2026-11-01", "end_date": "2026-11-02"})
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._create_reservation_from_file(str(rpath), store)
        self.assertIn("Reservation", f.getvalue())

    def test_create_reservation_from_file_negative_bad_json(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        bad = Path(self.tmpdir.name) / "bad_r.json"
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{ bad }")
        with self.assertRaises(SystemExit) as cm:
            self.cli._create_reservation_from_file(str(bad), store)
        self.assertEqual(cm.exception.code, 2)

    # delete/show/modify hotel helpers
    def test_delete_show_modify_hotel_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 6, "name": "H6", "address": "A", "rooms": {}})
        store.create_hotel(h)
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._show_hotel_by_id(6, store)
            self.cli._delete_hotel_by_id(6, store)
        out = f.getvalue()
        self.assertIn("Hotel 6", out)
        # modify non-existing should report not found
        badpath = Path(self.tmpdir.name) / "mh.json"
        self._write(str(badpath), {"hotel_id": 999, "name": "X", "address": "A", "rooms": {}})
        f2 = io.StringIO()
        with redirect_stdout(f2):
            self.cli._modify_hotel_from_file(str(badpath), store)
        self.assertIn("not found", f2.getvalue())

    def test_delete_show_modify_hotel_negative(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._show_hotel_by_id(9999, store)
            self.cli._delete_hotel_by_id(9999, store)
        out = f.getvalue()
        self.assertIn("not found", out)

    # cancel reservation
    def test_cancel_reservation_positive_and_negative(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        # prepare
        store.create_hotel(self.Hotel.from_dict({"hotel_id": 7, "name": "H7", "address": "A", "rooms": {"1": 1}}))
        store.create_customer(self.Customer.from_dict({"customer_id": 8, "name": "C8", "email": "e", "phone": "p"}))
        store.create_reservation(self.Reservation.from_dict({"reservation_id": 9, "customer_id": 8, "hotel_id": 7, "room_number": "1", "start_date": "2026-12-01", "end_date": "2026-12-02"}))
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._cancel_reservation_by_id(9, store)
            self.cli._cancel_reservation_by_id(9999, store)
        out = f.getvalue()
        self.assertIn("canceled", out)

    # delete/show/modify customer helpers
    def test_delete_show_modify_customer_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 10, "name": "C10", "email": "e", "phone": "p"})
        store.create_customer(c)
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._show_customer_by_id(10, store)
            self.cli._delete_customer_by_id(10, store)
        self.assertIn("Customer 10", f.getvalue())

    def test_delete_show_modify_customer_negative(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli._show_customer_by_id(9999, store)
            self.cli._delete_customer_by_id(9999, store)
        self.assertIn("not found", f.getvalue())

    # Integration tests that invoke main() to exercise argparse paths
    def test_main_create_all_positive(self) -> None:
        self._write(self.hotels, [])
        self._write(self.customers, [])
        self._write(self.reservations, [])
        hfile = Path(self.tmpdir.name) / "new_h.json"
        cfile = Path(self.tmpdir.name) / "new_c.json"
        rfile = Path(self.tmpdir.name) / "new_r.json"
        self._write(str(hfile), {"hotel_id": 21, "name": "H21", "address": "A", "rooms": {}})
        self._write(str(cfile), {"customer_id": 22, "name": "C22", "email": "e", "phone": "p"})
        self._write(str(rfile), {"reservation_id": 31, "customer_id": 22, "hotel_id": 21, "room_number": "1", "start_date": "2026-01-01", "end_date": "2026-01-02"})
        argv = [
            "--hotels",
            self.hotels,
            "--customers",
            self.customers,
            "--reservations",
            self.reservations,
            "--create-hotel",
            str(hfile),
            "--create-customer",
            str(cfile),
            "--create-reservation",
            str(rfile),
        ]
        f = io.StringIO()
        with redirect_stdout(f):
            rc = self.cli.main(argv)
        out = f.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Hotel created", out)
        self.assertIn("Customer created", out)

    def test_main_create_all_negative_bad_customer(self) -> None:
        self._write(self.hotels, [])
        self._write(self.customers, [])
        self._write(self.reservations, [])
        bad = Path(self.tmpdir.name) / "bad_c.json"
        with open(bad, "w", encoding="utf-8") as fh:
            fh.write("{ invalid }")
        argv = [
            "--hotels",
            self.hotels,
            "--customers",
            self.customers,
            "--reservations",
            self.reservations,
            "--create-customer",
            str(bad),
        ]
        with self.assertRaises(SystemExit) as cm:
            self.cli.main(argv)
        self.assertEqual(cm.exception.code, 2)

    def test_main_modify_and_delete_hotel_via_flags(self) -> None:
        self._write(self.hotels, [{"hotel_id": 40, "name": "H40", "address": "A", "rooms": {}}])
        self._write(self.customers, [])
        self._write(self.reservations, [])
        mod = Path(self.tmpdir.name) / "mod_h.json"
        self._write(str(mod), {"hotel_id": 40, "name": "H40-new", "address": "A", "rooms": {}})
        argv = [
            "--hotels",
            self.hotels,
            "--customers",
            self.customers,
            "--reservations",
            self.reservations,
            "--modify-hotel",
            str(mod),
            "--show-hotel",
            "40",
            "--delete-hotel",
            "40",
        ]
        f = io.StringIO()
        with redirect_stdout(f):
            rc = self.cli.main(argv)
        out = f.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Hotel updated", out)

    def test_main_customer_modify_and_delete_via_flags(self) -> None:
        self._write(self.hotels, [])
        self._write(self.customers, [{"customer_id": 50, "name": "C50", "email": "e", "phone": "p"}])
        self._write(self.reservations, [])
        modc = Path(self.tmpdir.name) / "mod_c.json"
        self._write(str(modc), {"customer_id": 50, "name": "C50-new", "email": "e", "phone": "p"})
        argv = [
            "--hotels",
            self.hotels,
            "--customers",
            self.customers,
            "--reservations",
            self.reservations,
            "--modify-customer",
            str(modc),
            "--show-customer",
            "50",
            "--delete-customer",
            "50",
        ]
        f = io.StringIO()
        with redirect_stdout(f):
            rc = self.cli.main(argv)
        out = f.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Customer updated", out)


if __name__ == "__main__":
    unittest.main()
