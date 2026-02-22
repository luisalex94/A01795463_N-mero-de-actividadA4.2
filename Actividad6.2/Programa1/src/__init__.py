"""Minimal package for the hotel reservation system.

Expose models and storage for external use.
"""
from .models import Customer, Hotel, Reservation
from .storage import Storage

__all__ = ["Customer", "Hotel", "Reservation", "Storage"]
