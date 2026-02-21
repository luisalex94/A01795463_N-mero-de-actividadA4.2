"""Hotel model module."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Hotel:
    """Represents a hotel with simple room inventory.

    Attributes:
        hotel_id: numeric identifier for the hotel.
        name: display name.
        address: text address.
        rooms: mapping room_number->capacity (int).
    """

    hotel_id: int
    name: str
    address: str
    rooms: Dict[str, int]

    def to_dict(self) -> Dict:
        """Return a JSON-serializable dict for this hotel."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Hotel":
        """Create a Hotel from a dictionary, raising ValueError on invalid."""
        try:
            hotel_id = int(data["hotel_id"])  # type: ignore[index]
            name = str(data["name"])  # type: ignore[index]
            address = str(data.get("address", ""))
            rooms = dict(data.get("rooms", {}))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Invalid hotel data") from error
        return cls(hotel_id=hotel_id, name=name, address=address, rooms=rooms)
