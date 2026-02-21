"""Reservation model module."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Reservation:
    """Reservation linking a customer, hotel and a room for a date range."""

    reservation_id: int
    customer_id: int
    hotel_id: int
    room_number: str
    start_date: str
    end_date: str

    def to_dict(self) -> Dict:
        """Return a JSON-serializable representation of this reservation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Reservation":
        """Create a Reservation from a dict or raise ValueError on invalid."""
        try:
            reservation_id = int(data["reservation_id"])  # type: ignore[index]
            customer_id = int(data["customer_id"])  # type: ignore[index]
            hotel_id = int(data["hotel_id"])  # type: ignore[index]
            room_number = str(data["room_number"])  # type: ignore[index]
            start_date = str(data["start_date"])  # type: ignore[index]
            end_date = str(data["end_date"])  # type: ignore[index]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Invalid reservation data") from error
        return cls(
            reservation_id=reservation_id,
            customer_id=customer_id,
            hotel_id=hotel_id,
            room_number=room_number,
            start_date=start_date,
            end_date=end_date,
        )
