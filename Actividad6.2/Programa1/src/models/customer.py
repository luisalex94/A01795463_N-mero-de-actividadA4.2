"""Customer model module."""
from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class Customer:
    """Customer information."""

    customer_id: int
    name: str
    email: str
    phone: str

    def to_dict(self) -> Dict:
        """Return a JSON-serializable representation of this customer."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Customer":
        """Create a Customer from a dict or raise ValueError on invalid."""
        try:
            customer_id = int(data["customer_id"])
            name = str(data["name"])
            email = str(data.get("email", ""))
            phone = str(data.get("phone", ""))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Invalid customer data") from error
        return (
            cls(
                customer_id=customer_id,
                name=name,
                email=email,
                phone=phone,
            )
        )
