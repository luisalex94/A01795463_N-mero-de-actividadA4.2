"""File-based storage and operations for hotels, customers and reservations.

This module provides the persistent behaviors requested: create/delete/
display/modify for hotels and customers, and create/cancel for
reservations. Invalid data in JSON files is tolerated (reported and
skipped) so execution continues.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .models import Customer, Hotel, Reservation


def _read_json_list(path: str) -> List[Dict]:
    """Read a JSON list from a file, returning list or empty list.

    If the file contains invalid JSON or the top-level value is not a
    list, an error is printed and an empty list is returned.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {path}: {error}")
        return []
    if not isinstance(data, list):
        print(f"Expected a list in {path}")
        return []
    return data


def _write_json_list(path: str, data: Iterable[Dict]) -> None:
    """Write an iterable of dicts to a JSON file as a list."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(list(data), handle, indent=2, ensure_ascii=False)


class Storage:
    """Manages files for hotels, customers and reservations.

    All file paths are plain JSON files containing lists of objects.
    """

    def __init__(
        self,
        hotels_path: str,
        customers_path: str,
        reservations_path: str,
    ) -> None:
        self.hotels_path = hotels_path
        self.customers_path = customers_path
        self.reservations_path = reservations_path

    # Hotel operations
    def list_hotels(self) -> List[Hotel]:
        """Return all valid hotels stored in the hotels file."""
        raw = _read_json_list(self.hotels_path)
        hotels: List[Hotel] = []
        for item in raw:
            try:
                hotels.append(Hotel.from_dict(item))
            except ValueError as exc:
                print(f"Skipping invalid hotel entry: {exc}")
        return hotels

    def create_hotel(self, hotel: Hotel) -> None:
        """Append a Hotel to the hotels file."""
        hotels = [h.to_dict() for h in self.list_hotels()]
        hotels.append(hotel.to_dict())
        _write_json_list(self.hotels_path, hotels)

    def delete_hotel(self, hotel_id: int) -> bool:
        """Delete a hotel by id; return True if removed."""
        kept = []
        found = False
        for h in self.list_hotels():
            if h.hotel_id == hotel_id:
                found = True
                continue
            kept.append(h.to_dict())
        if found:
            _write_json_list(self.hotels_path, kept)
        return found

    def get_hotel(self, hotel_id: int) -> Optional[Hotel]:
        """Return a Hotel by id or None if not present."""
        for h in self.list_hotels():
            if h.hotel_id == hotel_id:
                return h
        return None

    def update_hotel(self, hotel: Hotel) -> bool:
        """Replace an existing hotel entry. Return True if updated."""
        updated = False
        out: List[Dict] = []
        for h in self.list_hotels():
            if h.hotel_id == hotel.hotel_id:
                out.append(hotel.to_dict())
                updated = True
            else:
                out.append(h.to_dict())
        if updated:
            _write_json_list(self.hotels_path, out)
        return updated

    # Customer operations
    def list_customers(self) -> List[Customer]:
        """Return all valid customers stored in the customers file."""
        raw = _read_json_list(self.customers_path)
        customers: List[Customer] = []
        for item in raw:
            try:
                customers.append(Customer.from_dict(item))
            except ValueError as exc:
                print(f"Skipping invalid customer entry: {exc}")
        return customers

    def create_customer(self, customer: Customer) -> None:
        """Append a Customer to the customers file."""
        customers = [c.to_dict() for c in self.list_customers()]
        customers.append(customer.to_dict())
        _write_json_list(self.customers_path, customers)

    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer by id; return True if removed."""
        kept = []
        found = False
        for c in self.list_customers():
            if c.customer_id == customer_id:
                found = True
                continue
            kept.append(c.to_dict())
        if found:
            _write_json_list(self.customers_path, kept)
        return found

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Return a Customer by id or None if not present."""
        for c in self.list_customers():
            if c.customer_id == customer_id:
                return c
        return None

    def update_customer(self, customer: Customer) -> bool:
        """Replace an existing customer entry. Return True if updated."""
        updated = False
        out: List[Dict] = []
        for c in self.list_customers():
            if c.customer_id == customer.customer_id:
                out.append(customer.to_dict())
                updated = True
            else:
                out.append(c.to_dict())
        if updated:
            _write_json_list(self.customers_path, out)
        return updated

    # Reservation operations
    def list_reservations(self) -> List[Reservation]:
        """Return all valid reservations stored in the reservations file."""
        raw = _read_json_list(self.reservations_path)
        reservations: List[Reservation] = []
        for item in raw:
            try:
                reservations.append(Reservation.from_dict(item))
            except ValueError as exc:
                print(f"Skipping invalid reservation entry: {exc}")
        return reservations

    def _overlaps(
        self, start_a: str, end_a: str, start_b: str, end_b: str
    ) -> bool:
        """Return True when two date intervals overlap (inclusive)."""
        fmt = "%Y-%m-%d"
        a1 = datetime.strptime(start_a, fmt)
        a2 = datetime.strptime(end_a, fmt)
        b1 = datetime.strptime(start_b, fmt)
        b2 = datetime.strptime(end_b, fmt)
        return not (a2 < b1 or b2 < a1)

    def create_reservation(self, reservation: Reservation) -> bool:
        """Create a reservation if possible. Return True on success."""
        # basic validation
        if self.get_customer(reservation.customer_id) is None:
            print("Unknown customer for reservation")
            return False
        if self.get_hotel(reservation.hotel_id) is None:
            print("Unknown hotel for reservation")
            return False
        # check room conflicts
        for r in self.list_reservations():
            conflict = (
                r.hotel_id == reservation.hotel_id
                and r.room_number == reservation.room_number
                and self._overlaps(
                    r.start_date,
                    r.end_date,
                    reservation.start_date,
                    reservation.end_date,
                )
            )
            if conflict:
                print("Room is already reserved in that date range")
                return False
        reservations = [r.to_dict() for r in self.list_reservations()]
        reservations.append(reservation.to_dict())
        _write_json_list(self.reservations_path, reservations)
        return True

    def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancel a reservation by id; return True if removed."""
        kept = []
        found = False
        for r in self.list_reservations():
            if r.reservation_id == reservation_id:
                found = True
                continue
            kept.append(r.to_dict())
        if found:
            _write_json_list(self.reservations_path, kept)
        return found
