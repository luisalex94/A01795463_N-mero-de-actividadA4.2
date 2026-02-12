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
from typing import Dict, Iterable, List, Tuple


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

def _group_sales(sales: Iterable[dict]) -> Dict[int, Dict]:
    """Group flat sales records by SALE_ID.

    Returns a mapping SALE_ID -> {"date": str, "lines": [records...]}
    """
    grouped: Dict[int, Dict] = {}
    for record in sales:
        try:
            sale_id = int(record["SALE_ID"])
            sale_date = record.get("SALE_Date", "")
            product = record["Product"]
            quantity = int(record["Quantity"])
        except (KeyError, TypeError, ValueError) as exc:
            print(f"Invalid sales record skipped: {exc} -> {record}")
            continue
        if sale_id not in grouped:
            grouped[sale_id] = {"date": sale_date, "lines": []}
        grouped[sale_id]["lines"].append({
            "product": product,
            "quantity": quantity,
        })
    return grouped

def _format_report(
    catalogue: Dict[str, float], grouped: Dict[int, Dict]
) -> Tuple[str, float]:
    """Build a human-readable report string and return (report, grand_total).

    Missing products are reported in the report and treated as zero cost.
    """
    lines: List[str] = []
    grand_total = 0.0
    for sale_id in sorted(grouped.keys()):
        sale = grouped[sale_id]
        date = sale.get("date", "")
        lines.append(f"Sale ID: {sale_id}  Date: {date}")
        lines.append("  Product	UnitPrice	Quantity	LineTotal")
        sale_total = 0.0
        for entry in sale["lines"]:
            product = entry["product"]
            qty = entry["quantity"]
            if product not in catalogue:
                msg = (
                    "Product not found in catalogue: '" + product + "' (Sale "
                    + str(sale_id) + ")"
                )
                print(msg)
                unit_price = 0.0
                note = " [MISSING]"
            else:
                unit_price = catalogue[product]
                note = ""
            line_total = unit_price * qty
            sale_total += line_total
            lines.append(
                f"  {product}\t{unit_price:.2f}\t{qty}\t{line_total:.2f}{note}"
            )
        lines.append(f"  Sale total: {sale_total:.2f}")
        lines.append("")
        grand_total += sale_total
    report = "\n".join(lines)
    return report, grand_total