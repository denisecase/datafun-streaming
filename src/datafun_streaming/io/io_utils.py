"""src/datafun_streaming/io/io_utils.py.

CSV and JSON helpers for streaming examples.
"""

# === IMPORTS ===

import csv
import json
from pathlib import Path
from typing import Any

from datafun_streaming.io.errors import missing_csv_file_message

# === EXPORTS ===

__all__ = [
    "append_csv_row",
    "format_message_for_log",
    "read_csv_as_lookup",
    "read_csv_rows",
    "row_to_json",
    "row_from_json",
]

# === DEFINE HELPER FUNCTIONS ===


def append_csv_row(path: Path, row: dict[str, Any], fieldnames: list[str]) -> None:
    """Append one row to a CSV file, writing the header first if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()

    with path.open(mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def format_message_for_log(message: dict[str, Any]) -> str:
    """Format one message dictionary for readable log output."""
    lines = ["{"]

    for key, value in message.items():
        lines.append(f"  {key}: {value}")

    lines.append("}")
    return "\n".join(lines)


def read_csv_as_lookup(
    path: Path,
    *,
    key_field: str,
    value_field: str,
) -> dict[str, Any]:
    """Read a CSV file into a key-value lookup dictionary.

    Arguments:
        path:        Path to the CSV file.
        key_field:   The column to use as the dictionary key.
        value_field: The column to use as the dictionary value.

    Returns:
        A dict mapping each key_field value to its value_field value.

    Example:
        region_lookup = read_csv_as_lookup(
            REGIONS_CSV, key_field="region_id", value_field="tax_rate_pct"
        )
        tax_rate = float(region_lookup["US-MO"]) / 100.0
    """
    rows = read_csv_rows(path)
    return {row[key_field]: row[value_field] for row in rows}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of string dictionaries."""
    if not path.exists():
        msg = missing_csv_file_message(path=path.as_posix())
        raise FileNotFoundError(msg)

    with path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            msg = f"CSV file has no header row: {path.as_posix()}"
            raise ValueError(msg)

        return list(reader)


def row_to_json(row: dict[str, Any]) -> str:
    """Convert a row dictionary to compact JSON text."""
    return json.dumps(row, sort_keys=True, separators=(",", ":"))


def row_from_json(text: str) -> dict[str, Any]:
    """Convert JSON text to a row dictionary."""
    value = json.loads(text)

    if not isinstance(value, dict):
        msg = "Expected JSON object."
        raise ValueError(msg)

    return value
