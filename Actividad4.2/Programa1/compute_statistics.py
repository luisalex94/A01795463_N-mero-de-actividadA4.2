"""This code provides utilities to read and make statistics from 
text files.

This program computes basic statistics (mean, median, mode, variance, 
standard deviation) from the numeric data extracted from the text files.
"""

from numbers import Number
import sys
from typing import List, Tuple, Iterator
import time
import os


def parse_number(num: str) -> Number:
    """Try to convert a token to int or float.

    Tries int first (so integers remain ints). If int() fails,
    tries float(). If that also fails, raises ValueError chaining
    the original exception for better traceability.

    Args:
        num: token string to parse.

    Returns:
        int or float parsed from the token.

    Raises:
        ValueError: if the token cannot be parsed as a number.
    """
    s = num.strip()
    try:
        return int(s)
    except ValueError:
        pass
    if '.' in s:
        left, right = s.split('.', 1)
        if right.strip('0') == '':
            try:
                return int(left)
            except ValueError:
                pass
    try:
        return float(s)
    except ValueError as exc:
        raise ValueError(f"Not a number: {num}") from exc


def tokens_from_line(line: str) -> Iterator[str]:
    """Yield tokens found on a line.

    This normalizes common separators (commas and semicolons) to spaces
    and then yields the whitespace-separated tokens. Using ``yield from``
    is a concise way to forward the tokens from ``split()``.
    """
    yield line.strip()


def read_numbers(file_path: str) -> Tuple[List[Number], List[Tuple[int, str]]]:
    """Read numbers from a file and collect invalid tokens.

    Args:
        file_path: path to the text file to read.

    Returns:
        A tuple (numbers, invalids) where `numbers` is a list of parsed
        int/float values and `invalids` is a list of (line_number, token)
        for tokens that couldn't be parsed.
    """
    numbers: List[Number] = []
    invalids: List[Tuple[int, str]] = []

    parser = parse_number

    with open(file_path, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            for tok in tokens_from_line(line):
                try:
                    val = parser(tok)
                    numbers.append(val)
                except ValueError:
                    invalids.append((lineno, tok))
                    print(f"Invalid number at line {lineno}: {tok}")
    return numbers, invalids


def compute_descriptive_stats(nums: List[Number]) -> dict:
    """Compute mean, median, mode(s), variance and stddev from nums.

    Returns a dict with keys: mean, median, mode (None or value/list),
    variance, stddev.
    """
    # mean
    total = 0.0
    for x in nums:
        total += float(x)
    mean = total / len(nums) if nums else 0.0

    # median
    sorted_nums = sorted(nums)
    if not sorted_nums:
        median = 0.0
    elif len(sorted_nums) % 2 == 1:
        median = sorted_nums[len(sorted_nums) // 2]
    else:
        median = (
            sorted_nums[len(sorted_nums) // 2 - 1]
            + sorted_nums[len(sorted_nums) // 2]
        ) / 2.0

    # mode
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    max_freq = max(counts.values()) if counts else 0
    if max_freq <= 1:
        mode = None
    else:
        mode = None
        for v in nums:
            if counts.get(v, 0) == max_freq:
                mode = v
                break

    # variance and stddev
    sum_sq = 0.0
    for x in nums:
        diff = float(x) - mean
        sum_sq += diff * diff
    variance = sum_sq / len(nums) if nums else 0.0
    stddev = variance ** 0.5

    # unbiased sample variance
    variance_sample = sum_sq / (len(nums) - 1) if len(nums) > 1 else 0.0

    return {
        "mean": mean,
        "median": median,
        "mode": mode,
        "stddev": stddev,
        "variance_sample": variance_sample,
    }


def write_results_file(file_path: str, stats: dict, elapsed: float, count: int) -> None:
    """Write the computed stats and elapsed time into StatisticsResults.txt.

    Writes the file next to the input file.
    """
    out_dir = os.path.dirname(os.path.abspath(file_path)) or "."
    out_path = os.path.join(out_dir, "StatisticsResults.txt")
    with open(out_path, "w", encoding="utf-8") as out:
        if stats and stats.get("mean") is not None:
            def format_num(v):
                if isinstance(v, int):
                    return str(v)
                if isinstance(v, float):
                    if v.is_integer():
                        return str(int(v))
                    s = f"{v:.12f}".rstrip('0').rstrip('.')
                    return s
                return str(v)

            out.write(f"COUNT {count}\n")
            out.write(f"MEAN {format_num(stats['mean'])}\n")
            out.write(f"MEDIAN {format_num(stats['median'])}\n")
            out.write(f"MODE {format_num(stats['mode'])}\n")
            out.write(f"SD {format_num(stats['stddev'])}\n")
            out.write(f"VARIANCE {format_num(stats['variance_sample'])}\n")
        else:
            out.write("No numbers found in input file.\n")
        out.write(f"Elapsed time (s): {elapsed:.6f}\n")


def process_file(file_path: str) -> int:
    """Read the file, compute statistics, print and write results.

    Returns 0 on success, non-zero on error.
    """
    start_time = time.time()

    nums, invalids = read_numbers(file_path)
    count = len(nums) + len(invalids)
    print(f"COUNT {count}")

    stats = compute_descriptive_stats(nums) if nums else compute_descriptive_stats([])
    def format_num(v):
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            if v.is_integer():
                return str(int(v))
            s = f"{v:.12f}".rstrip('0').rstrip('.')
            return s
        return str(v)

    if nums:
        print(f"MEAN {format_num(stats['mean'])}")
        print(f"MEDIAN {format_num(stats['median'])}")
        print(f"MODE {format_num(stats['mode'])}")
        print(f"SD {format_num(stats['stddev'])}")
        print(f"VARIANCE {format_num(stats['variance_sample'])}")
    else:
        print("No se encontraron números en el archivo.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")

    write_results_file(file_path, stats, elapsed_time, count)
    return 0


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not input_path:
        print("Usage: python compute_statistics.py <file_path>")
        sys.exit(1)
    sys.exit(process_file(input_path))
