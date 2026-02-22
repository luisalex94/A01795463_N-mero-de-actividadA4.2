"""Unit tests for Storage: one positive and one negative test per method.

These tests exercise the public API of `src.storage.Storage` and use
temporary files to avoid modifying repository data.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


class StoragePerMethodTests(unittest.TestCase):
    """Each Storage method is exercised with a positive and negative test."""

    def setUp(self) -> None:
        # Make local package importable
        import sys

        project_dir = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(project_dir))

        # Import under test after sys.path adjusted
        from src.storage import Storage
        from src.models import Hotel, Customer, Reservation

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

    # --- Hotels: list, create, get, update, delete ---
    def test_list_hotels_positive(self) -> None:
        self._write(self.hotels, [{"hotel_id": 1, "name": "H", "address": "A", "rooms": {}}])
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(len(store.list_hotels()), 1)

    def test_list_hotels_negative_invalid_json(self) -> None:
        with open(self.hotels, "w", encoding="utf-8") as fh:
            fh.write("{ not json }")
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(store.list_hotels(), [])

    def test_create_hotel_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 2, "name": "H2", "address": "A", "rooms": {}})
        store.create_hotel(h)
        self.assertIsNotNone(store.get_hotel(2))

    def test_create_hotel_negative_when_file_contains_nonlist(self) -> None:
        self._write(self.hotels, {"not": "a list"})
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 3, "name": "H3", "address": "A", "rooms": {}})
        store.create_hotel(h)
        self.assertIsNotNone(store.get_hotel(3))

    def test_get_hotel_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 4, "name": "H4", "address": "A", "rooms": {}})
        store.create_hotel(h)
        self.assertEqual(store.get_hotel(4).hotel_id, 4)

    def test_get_hotel_negative_not_found(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertIsNone(store.get_hotel(999))

    def test_update_hotel_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 5, "name": "H5", "address": "A", "rooms": {}})
        store.create_hotel(h)
        h.name = "Updated"
        self.assertTrue(store.update_hotel(h))
        self.assertEqual(store.get_hotel(5).name, "Updated")

    def test_update_hotel_negative_not_existing(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 6, "name": "H6", "address": "A", "rooms": {}})
        self.assertFalse(store.update_hotel(h))

    def test_delete_hotel_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 7, "name": "H7", "address": "A", "rooms": {}})
        store.create_hotel(h)
        self.assertTrue(store.delete_hotel(7))

    def test_delete_hotel_negative_not_found(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertFalse(store.delete_hotel(12345))

    # --- Customers: list, create, get, update, delete ---
    def test_list_customers_positive(self) -> None:
        self._write(self.customers, [{"customer_id": 10, "name": "C", "email": "e", "phone": "p"}])
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(len(store.list_customers()), 1)

    def test_list_customers_negative_invalid_json(self) -> None:
        with open(self.customers, "w", encoding="utf-8") as fh:
            fh.write("{ invalid }")
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(store.list_customers(), [])

    def test_create_customer_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 11, "name": "C11", "email": "e", "phone": "p"})
        store.create_customer(c)
        self.assertIsNotNone(store.get_customer(11))

    def test_create_customer_negative_nonlist_file(self) -> None:
        self._write(self.customers, {"foo": "bar"})
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 12, "name": "C12", "email": "e", "phone": "p"})
        store.create_customer(c)
        self.assertIsNotNone(store.get_customer(12))

    def test_get_customer_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 13, "name": "C13", "email": "e", "phone": "p"})
        store.create_customer(c)
        self.assertEqual(store.get_customer(13).customer_id, 13)

    def test_get_customer_negative_not_found(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertIsNone(store.get_customer(9999))

    def test_update_customer_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 14, "name": "C14", "email": "e", "phone": "p"})
        store.create_customer(c)
        c.name = "C14-new"
        self.assertTrue(store.update_customer(c))
        self.assertEqual(store.get_customer(14).name, "C14-new")

    def test_update_customer_negative_not_existing(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 15, "name": "C15", "email": "e", "phone": "p"})
        self.assertFalse(store.update_customer(c))

    def test_delete_customer_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        c = self.Customer.from_dict({"customer_id": 16, "name": "C16", "email": "e", "phone": "p"})
        store.create_customer(c)
        self.assertTrue(store.delete_customer(16))

    def test_delete_customer_negative_not_found(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertFalse(store.delete_customer(4242))

    # --- Reservations: list, create, cancel, overlaps ---
    def test_list_reservations_positive(self) -> None:
        self._write(self.reservations, [{"reservation_id": 1, "customer_id": 1, "hotel_id": 1, "room_number": "1", "start_date": "2026-01-01", "end_date": "2026-01-02"}])
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(len(store.list_reservations()), 1)

    def test_list_reservations_negative_invalid_json(self) -> None:
        with open(self.reservations, "w", encoding="utf-8") as fh:
            fh.write("{ bad }")
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertEqual(store.list_reservations(), [])

    def test_overlaps_positive_and_negative(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertTrue(store._overlaps("2026-02-01", "2026-02-05", "2026-02-04", "2026-02-06"))
        self.assertFalse(store._overlaps("2026-02-01", "2026-02-05", "2026-02-06", "2026-02-10"))

    def test_create_reservation_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 20, "name": "H20", "address": "A", "rooms": {"1": 1}})
        c = self.Customer.from_dict({"customer_id": 21, "name": "C21", "email": "e", "phone": "p"})
        store.create_hotel(h)
        store.create_customer(c)
        r = self.Reservation.from_dict({"reservation_id": 30, "customer_id": 21, "hotel_id": 20, "room_number": "1", "start_date": "2026-08-01", "end_date": "2026-08-02"})
        self.assertTrue(store.create_reservation(r))

    def test_create_reservation_negative_unknown_refs(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        r = self.Reservation.from_dict({"reservation_id": 31, "customer_id": 9999, "hotel_id": 8888, "room_number": "1", "start_date": "2026-09-01", "end_date": "2026-09-02"})
        self.assertFalse(store.create_reservation(r))

    def test_cancel_reservation_positive(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        h = self.Hotel.from_dict({"hotel_id": 40, "name": "H40", "address": "A", "rooms": {"1": 1}})
        c = self.Customer.from_dict({"customer_id": 41, "name": "C41", "email": "e", "phone": "p"})
        store.create_hotel(h)
        store.create_customer(c)
        r = self.Reservation.from_dict({"reservation_id": 50, "customer_id": 41, "hotel_id": 40, "room_number": "1", "start_date": "2026-10-01", "end_date": "2026-10-02"})
        self.assertTrue(store.create_reservation(r))
        self.assertTrue(store.cancel_reservation(50))

    def test_cancel_reservation_negative_not_found(self) -> None:
        store = self.Storage(self.hotels, self.customers, self.reservations)
        self.assertFalse(store.cancel_reservation(7777))


if __name__ == "__main__":
    unittest.main()
