"""Tests for datafun_streaming.io.io_utils."""

import json
from pathlib import Path

import pytest

from datafun_streaming.io.io_utils import (
    append_csv_row,
    format_message_for_log,
    read_csv_as_lookup,
    read_csv_rows,
    row_from_json,
    row_to_json,
)

# === row_to_json / row_from_json ===


def test_row_to_json_produces_valid_json() -> None:
    row = {"sale_id": "S001", "amount": 99.99}
    result = row_to_json(row)
    parsed = json.loads(result)
    assert parsed["sale_id"] == "S001"


def test_row_to_json_is_sorted() -> None:
    row = {"z_field": "z", "a_field": "a"}
    result = row_to_json(row)
    assert result.index("a_field") < result.index("z_field")


def test_row_from_json_round_trips() -> None:
    row = {"sale_id": "S001", "region_id": "US-MO"}
    assert row_from_json(row_to_json(row)) == row


def test_row_from_json_raises_on_non_object() -> None:
    with pytest.raises(ValueError, match="Expected JSON object"):
        row_from_json("[1, 2, 3]")


# === read_csv_rows ===


def test_read_csv_rows_returns_list(tmp_path: Path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("sale_id,region_id\nS001,US-MO\nS002,US-KS\n")
    rows = read_csv_rows(csv_file)
    assert len(rows) == 2
    assert rows[0]["sale_id"] == "S001"


def test_read_csv_rows_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_csv_rows(tmp_path / "nonexistent.csv")


def test_read_csv_rows_empty_file_raises(tmp_path: Path) -> None:
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    with pytest.raises(ValueError, match="no header row"):
        read_csv_rows(csv_file)


# === read_csv_as_lookup ===


def test_read_csv_as_lookup(tmp_path: Path) -> None:
    csv_file = tmp_path / "regions.csv"
    csv_file.write_text("region_id,tax_rate_pct\nUS-MO,8.5\nUS-KS,6.5\n")
    lookup = read_csv_as_lookup(
        csv_file, key_field="region_id", value_field="tax_rate_pct"
    )
    assert lookup["US-MO"] == "8.5"
    assert lookup["US-KS"] == "6.5"


# === append_csv_row ===


def test_append_csv_row_creates_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "output.csv"
    append_csv_row(csv_file, {"sale_id": "S001"}, fieldnames=["sale_id"])
    assert csv_file.exists()


def test_append_csv_row_writes_header_once(tmp_path: Path) -> None:
    csv_file = tmp_path / "output.csv"
    append_csv_row(csv_file, {"sale_id": "S001"}, fieldnames=["sale_id"])
    append_csv_row(csv_file, {"sale_id": "S002"}, fieldnames=["sale_id"])
    rows = read_csv_rows(csv_file)
    assert len(rows) == 2


# === format_message_for_log ===


def test_format_message_for_log_contains_keys_and_values() -> None:
    message = {"sale_id": "S001", "region_id": "US-MO"}
    result = format_message_for_log(message)
    assert "sale_id" in result
    assert "S001" in result
    assert "region_id" in result
