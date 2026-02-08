"""Count distinct words in a file and write the frequencies.

Usage:
    python word_count.py fileWithData.txt

The program reads tokens separated by whitespace and validates tokens
as simple words (alphanumeric, at least one character). It counts
occurrences using basic algorithms, prints the results to the console
and writes them to ``WordCountResults.txt``. Invalid tokens are
reported on the console and ignored for counting. The elapsed time is
printed and appended to the results file.
"""

from __future__ import annotations

import sys
import time
from typing import Dict, Iterable, Tuple


def _is_valid_token(token: str) -> bool:
    """Return True if token is a valid word token.

    A valid token contains only alphanumeric characters (letters/digits)
    and is not empty. This is a conservative check that can be adapted
    if your input has other valid forms.
    """
    return bool(token) and token.isalnum()


def process_file(input_path: str, output_path: str = "WordCountResults.txt") -> Tuple[int, float]:
    """Process `input_path`, write results to `output_path`.

    Returns a tuple (total_tokens_counted, elapsed_seconds).
    """
    start = time.perf_counter()
    counts, total, invalid_count = _read_and_count(input_path)
    _write_results(counts, total, invalid_count, output_path)
    elapsed = time.perf_counter() - start
    summary = f"Elapsed time: {elapsed:.6f} seconds\n"
    print(summary, end="")
    with open(output_path, "a", encoding="utf-8") as outfile:
        outfile.write(summary)
    return total, elapsed


def _read_and_count(input_path: str) -> Tuple[Dict[str, int], int, int]:
    """Read file and return (counts, total, invalid_count)."""
    total = 0
    invalid_count = 0
    counts: Dict[str, int] = {}
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            for lineno, raw in enumerate(infile, start=1):
                for part in raw.split():
                    token = part.strip()
                    if not _is_valid_token(token):
                        print(f"Line {lineno}: invalid token -> '{token}'")
                        invalid_count += 1
                        continue
                    if token in counts:
                        counts[token] += 1
                    else:
                        counts[token] = 1
                    total += 1
    except OSError as exc:
        print(f"Error opening input file: {exc}")
        raise
    return counts, total, invalid_count


def _write_results(
    counts: Dict[str, int],
    total: int,
    invalid_count: int,
    output_path: str,
) -> None:
    """Write counts and totals into `output_path`.

    The function writes results deterministically sorted by token.
    """
    sorted_items = sorted(counts.items(), key=lambda item: item[0])
    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write("Word\tCount\n")
            for word, cnt in sorted_items:
                line = f"{word}\t{cnt}"
                print(line)
                outfile.write(f"{line}\n")
            grand_line = f"Grand Total\t{total}"
            print(grand_line)
            outfile.write(f"{grand_line}\n")
            if invalid_count:
                inval_line = f"Invalid tokens ignored\t{invalid_count}"
                print(inval_line)
                outfile.write(f"{inval_line}\n")
    except OSError as exc:
        print(f"Error writing output file: {exc}")
        raise


def _main(argv: Iterable[str]) -> int:
    """Command-line entry point. Returns exit code.

    Expected invocation: python word_count.py fileWithData.txt
    """
    argv_list = list(argv)
    if len(argv_list) != 2:
        print("Usage: python word_count.py fileWithData.txt")
        return 2
    input_file = argv_list[1]
    try:
        process_file(input_file)
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
