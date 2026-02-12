"""Compute total sales cost using a product catalogue and sales records.

Usage:
    python compute_sales.py priceCatalogue.json salesRecord.json

The program reads a catalogue JSON (list of products with prices) and a
sales JSON (list of sale lines). It computes per-sale totals and a grand
total, prints a human-readable report to the console and writes the
same report to ``SalesResults.txt``. Invalid entries are reported and
skipped; execution continues.
"""


import json
from typing import Dict


def _load_catalogue(path: str) -> Dict[str, float]:
    """Load product catalogue and return mapping title -> price.

    Raises OSError on I/O errors or ValueError for invalid JSON.
    Invalid product entries (missing price or title) are ignored with a
    console message.
    """
    catalogue: Dict[str, float] = {}
    with open(path, "r", encoding="utf-8") as infile:
        data = json.load(infile)
    if not isinstance(data, list):
        raise ValueError("Catalogue JSON must be a list of products")
    for item in data:
        try:
            title = item["title"]
            price = float(item["price"])
        except (KeyError, TypeError, ValueError) as exc:
            print(f"Invalid product entry in catalogue: {exc}")
            continue
        catalogue[title] = price
    return catalogue