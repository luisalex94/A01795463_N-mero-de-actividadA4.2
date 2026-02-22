"""Simple CLI wrapper to exercise Storage with file arguments.

Usage examples:
    python storage.py sample_data/hotels.json \
        sample_data/customers.json sample_data/reservations.json
    python storage.py --hotels hotels.json \
        --customers customers.json --reservations reservations.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional

from src.storage import Storage
from src.models import Hotel, Customer, Reservation


def _detect_files(positional: list[str]) -> Dict[str, str]:
    """Try to map three positional files to hotels/customers/reservations."""
    mapping: Dict[str, Optional[str]] = {
        "hotels": None,
        "customers": None,
        "reservations": None,
    }
    for p in positional:
        name = Path(p).name.lower()
        if "hotel" in name:
            mapping["hotels"] = p
        elif "customer" in name:
            mapping["customers"] = p
        elif "reservation" in name:
            mapping["reservations"] = p

    if all(mapping.values()):
        return {k: v for k, v in mapping.items() if v}

    if len(positional) >= 3:
        return {
            "hotels": positional[0],
            "customers": positional[1],
            "reservations": positional[2],
        }
    raise SystemExit("Please provide three files or use the keyword options.")


def _create_hotel_from_file(path: str, store: Storage) -> None:
    """Read a hotel JSON file, validate and append it using Storage."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        hotel = Hotel.from_dict(data)
        store.create_hotel(hotel)
        print("Hotel created")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error creating hotel: {exc}")
        raise SystemExit(2) from exc


def _create_customer_from_file(path: str, store: Storage) -> None:
    """Read a customer JSON file, validate and append it using Storage."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        customer = Customer.from_dict(data)
        store.create_customer(customer)
        print("Customer created")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error creating customer: {exc}")
        raise SystemExit(2) from exc


def _create_reservation_from_file(path: str, store: Storage) -> None:
    """Read a reservation JSON file, validate and append it using Storage."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        reservation = Reservation.from_dict(data)
        if store.create_reservation(reservation):
            print("Reservation created")
        else:
            print("Reservation could not be created (conflict or invalid ref)")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error creating reservation: {exc}")
        raise SystemExit(2) from exc


def _execute_actions(args: argparse.Namespace, store: Storage) -> None:
    """Orchestrate all requested actions from CLI arguments."""
    # Creation actions
    if args.create_hotel:
        _create_hotel_from_file(args.create_hotel, store)
    if args.create_customer:
        _create_customer_from_file(args.create_customer, store)
    if args.create_reservation:
        _create_reservation_from_file(args.create_reservation, store)

    # Hotel actions
    if args.modify_hotel:
        _modify_hotel_from_file(args.modify_hotel, store)
    if args.show_hotel:
        _show_hotel_by_id(args.show_hotel, store)
    if args.delete_hotel:
        _delete_hotel_by_id(args.delete_hotel, store)

    # Customer actions
    if args.modify_customer:
        _modify_customer_from_file(args.modify_customer, store)
    if args.show_customer:
        _show_customer_by_id(args.show_customer, store)
    if args.delete_customer:
        _delete_customer_by_id(args.delete_customer, store)

    # Reservation actions
    if args.cancel_reservation:
        _cancel_reservation_by_id(args.cancel_reservation, store)


def _delete_hotel_by_id(hotel_id: int, store: Storage) -> None:
    """Delete a hotel by id and report the result."""
    if store.delete_hotel(hotel_id):
        print(f"Hotel {hotel_id} deleted")
    else:
        print(f"Hotel {hotel_id} not found")


def _show_hotel_by_id(hotel_id: int, store: Storage) -> None:
    """Display hotel information as JSON to stdout."""
    hotel = store.get_hotel(hotel_id)
    if hotel:
        print(hotel.to_dict())
    else:
        print(f"Hotel {hotel_id} not found")


def _modify_hotel_from_file(path: str, store: Storage) -> None:
    """Read a hotel JSON file and replace existing hotel entry."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        hotel = Hotel.from_dict(data)
        if store.update_hotel(hotel):
            print("Hotel updated")
        else:
            print("Hotel not found; nothing updated")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error modifying hotel: {exc}")
        raise SystemExit(2) from exc


def _cancel_reservation_by_id(reservation_id: int, store: Storage) -> None:
    """Cancel a reservation by id and print the result."""
    if store.cancel_reservation(reservation_id):
        print(f"Reservation {reservation_id} canceled")
    else:
        print(f"Reservation {reservation_id} not found")


def _delete_customer_by_id(customer_id: int, store: Storage) -> None:
    """Delete a customer by id and report the result."""
    if store.delete_customer(customer_id):
        print(f"Customer {customer_id} deleted")
    else:
        print(f"Customer {customer_id} not found")


def _show_customer_by_id(customer_id: int, store: Storage) -> None:
    """Display customer information as JSON to stdout."""
    customer = store.get_customer(customer_id)
    if customer:
        print(customer.to_dict())
    else:
        print(f"Customer {customer_id} not found")


def _modify_customer_from_file(path: str, store: Storage) -> None:
    """Read a customer JSON file and replace existing customer entry."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        customer = Customer.from_dict(data)
        if store.update_customer(customer):
            print("Customer updated")
        else:
            print("Customer not found; nothing updated")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error modifying customer: {exc}")
        raise SystemExit(2) from exc


def _get_parser() -> argparse.ArgumentParser:
    """Initialize and return the argument parser."""
    parser = argparse.ArgumentParser(prog="storage.py")
    parser.add_argument("files", nargs="*", help="Positional files")
    parser.add_argument("--hotels", help="Hotels JSON file path")
    parser.add_argument("--customers", help="Customers JSON file path")
    parser.add_argument("--reservations", help="Reservations JSON file path")
    parser.add_argument("--create-hotel", help="Path to hotel JSON.")
    parser.add_argument("--create-customer", help="Path to customer JSON.")
    parser.add_argument(
        "--create-reservation", help="Path to reservation JSON."
    )
    parser.add_argument("--delete-hotel", type=int, help="Delete hotel by id")
    parser.add_argument("--show-hotel", type=int, help="Show hotel by id")
    parser.add_argument("--modify-hotel", help="Path to hotel JSON to update.")
    parser.add_argument(
        "--cancel-reservation", type=int, help="Cancel res by id"
    )
    parser.add_argument(
        "--delete-customer", type=int, help="Delete cust by id"
    )
    parser.add_argument("--show-customer", type=int, help="Show cust by id")
    parser.add_argument(
        "--modify-customer", help="Path to cust JSON to update."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = _get_parser().parse_args(argv or sys.argv[1:])

    if args.hotels and args.customers and args.reservations:
        h_p, c_p, r_p = args.hotels, args.customers, args.reservations
    else:
        detected = _detect_files(args.files or [])
        h_p = detected.get("hotels")  # type: ignore
        c_p = detected.get("customers")  # type: ignore
        r_p = detected.get("reservations")

    store = Storage(h_p, c_p, r_p)
    _execute_actions(args, store)

    print("Loaded:")
    print(f" Hotels: {len(store.list_hotels())}")
    print(f" Customers: {len(store.list_customers())}")
    print(f" Reservations: {len(store.list_reservations())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
