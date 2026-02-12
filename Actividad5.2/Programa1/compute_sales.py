"""Compute total sales cost using a product catalogue and sales records.

Usage:
    python compute_sales.py priceCatalogue.json salesRecord.json

The program reads a catalogue JSON (list of products with prices) and a
sales JSON (list of sale lines). It computes per-sale totals and a grand
total, prints a human-readable report to the console and writes the
same report to ``SalesResults.txt``. Invalid entries are reported and
skipped; execution continues.
"""
