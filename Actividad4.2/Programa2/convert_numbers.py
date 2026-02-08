
"""Convert numbers from a file to binary and hexadecimal.

Usage:
    python convert_numbers.py fileWithData.txt

This module implements manual algorithms to convert integers to binary
and hexadecimal representations without using built-in conversion
functions like ``bin`` or ``hex``. Negative integers are represented
in 32-bit two's complement for the hexadecimal output and for binary
as well (32 bits) to be consistent. Errors in the input file are
reported to the console and the program continues processing
remaining lines. Results are printed to the console and written to
``ConvertionResults.txt``.
"""

from __future__ import annotations

import sys
import time
from typing import Iterable


def _int_to_binary_unsigned(value: int) -> str:
    """Return binary representation for a non-negative integer.

    The result contains no leading zeros except for the value 0.
    """
    if value == 0:
        return "0"
    bits: list[str] = []
    while value > 0:
        bits.append("1" if (value & 1) else "0")
        value >>= 1
    bits.reverse()
    return "".join(bits)


def _int_to_hex_unsigned(value: int) -> str:
    """Return hexadecimal (uppercase) string for a non-negative integer.

    The result contains no leading zeros except for the value 0.
    """
    if value == 0:
        return "0"
    hex_digits = "0123456789ABCDEF"
    parts: list[str] = []
    while value > 0:
        parts.append(hex_digits[value & 0xF])
        value >>= 4
    parts.reverse()
    return "".join(parts)


def dec_to_binary(value: int) -> str:
    """Convert signed integer to a binary string.

    For negative values the 32-bit two's complement representation is
    returned as a 32-character string.
    """
    if value >= 0:
        return _int_to_binary_unsigned(value)
    masked = value & 0xFFFFFFFF
    bits: list[str] = []
    for bit in range(31, -1, -1):
        bits.append("1" if (masked >> bit) & 1 else "0")
    return "".join(bits)


def dec_to_hex(value: int) -> str:
    """Convert signed integer to hexadecimal string.

    For negative values an 8-digit uppercase 32-bit two's complement
    representation is returned. Non-negative values use the minimal
    uppercase representation (no leading zeros except for zero).
    """
    if value >= 0:
        return _int_to_hex_unsigned(value)
    masked = value & 0xFFFFFFFF
    result = _int_to_hex_unsigned(masked)
    return result.rjust(8, "0")


def process_file(input_path: str, output_path: str = "ConvertionResults.txt") -> float:
    """Read numbers from ``input_path`` and write conversions to
    ``output_path``.

    Returns the elapsed time in seconds.
    """
    start = time.perf_counter()
    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", encoding="utf-8"
    ) as outfile:
        index = 0
        for raw in infile:
            index += 1
            line = raw.strip()
            if line == "":
                continue
            try:
                number = int(line)
            except ValueError:
                print(f"Line {index}: invalid integer -> '{line}'")
                out_line = f"{index}\t{line}\t#VALUE!\t#VALUE!\n"
                outfile.write(out_line)
                continue

            binary = dec_to_binary(number)
            hexa = dec_to_hex(number)
            out_line = f"{index}\t{number}\t{binary}\t{hexa}\n"
            print(out_line, end="")
            outfile.write(out_line)

    elapsed = time.perf_counter() - start
    summary = f"Elapsed time: {elapsed:.6f} seconds\n"
    print(summary, end="")
    with open(output_path, "a", encoding="utf-8") as outfile:
        outfile.write(summary)
    return elapsed


def _main(argv: Iterable[str]) -> int:
    """Command-line entry point. Returns exit code.

    Expected invocation: python convert_numbers.py fileWithData.txt
    """
    argv_list = list(argv)
    if len(argv_list) != 2:
        print("Usage: python convert_numbers.py fileWithData.txt")
        return 2
    input_file = argv_list[1]
    try:
        process_file(input_file)
    except OSError as exc:
        print(f"I/O error during processing: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
