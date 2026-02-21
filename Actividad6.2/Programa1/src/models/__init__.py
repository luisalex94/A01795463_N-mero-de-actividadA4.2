"""Models package: re-export model classes for convenient imports.

This package exposes the classes defined in the per-class modules so
callers can ``from src.models import Hotel, Customer, Reservation`` and
receive the class objects (not the submodules).
"""
from .hotel import Hotel  # re-export class for package consumers
from .customer import Customer  # re-export class for package consumers
from .reservation import Reservation  # re-export class for package consumers

__all__ = ["Hotel", "Customer", "Reservation"]
