"""Tests for datafun_streaming.storage.duckdb_utils."""

from pathlib import Path

import pytest

from datafun_streaming.storage.duckdb_utils import (
    close_db,
    init_db,
    query_db,
    safe_table_name,
    upsert_row,
)

ALLOWED: frozenset[str] = frozenset({"sales", "rejected"})


# === safe_table_name ===


def test_safe_table_name_valid() -> None:
    assert safe_table_name("sales", ALLOWED) == "sales"


def test_safe_table_name_invalid_raises() -> None:
    with pytest.raises(ValueError, match="not in the allowed list"):
        safe_table_name("drop_table", ALLOWED)


# === init_db / close_db ===


def test_init_db_creates_file(tmp_path: Path) -> None:
    db_path = tmp_path / "test.duckdb"
    conn = init_db(db_path)
    assert db_path.exists()
    close_db(conn)


def test_init_db_creates_parent_dirs(tmp_path: Path) -> None:
    db_path = tmp_path / "nested" / "dir" / "test.duckdb"
    conn = init_db(db_path)
    assert db_path.exists()
    close_db(conn)


# === upsert_row / query_db ===


def test_upsert_row_inserts_new_row(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "test.duckdb")
    row = {"sale_id": "S001", "region_id": "US-MO", "amount": 99.99}
    upsert_row(
        conn, table="sales", row=row, primary_key="sale_id", allowed_tables=ALLOWED
    )
    results = query_db(conn, "SELECT * FROM sales")
    assert len(results) == 1
    assert results[0]["sale_id"] == "S001"
    close_db(conn)


def test_upsert_row_replaces_existing_row(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "test.duckdb")
    row1 = {"sale_id": "S001", "region_id": "US-MO", "amount": 50.0}
    row2 = {"sale_id": "S001", "region_id": "US-KS", "amount": 75.0}
    upsert_row(
        conn, table="sales", row=row1, primary_key="sale_id", allowed_tables=ALLOWED
    )
    upsert_row(
        conn, table="sales", row=row2, primary_key="sale_id", allowed_tables=ALLOWED
    )
    results = query_db(conn, "SELECT * FROM sales")
    assert len(results) == 1
    assert results[0]["region_id"] == "US-KS"
    close_db(conn)


def test_upsert_row_rejects_invalid_table(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "test.duckdb")
    with pytest.raises(ValueError):
        upsert_row(
            conn,
            table="malicious_table",
            row={"sale_id": "S001"},
            primary_key="sale_id",
            allowed_tables=ALLOWED,
        )
    close_db(conn)


def test_query_db_returns_empty_list(tmp_path: Path) -> None:
    conn = init_db(tmp_path / "test.duckdb")
    row = {"sale_id": "S001", "region_id": "US-MO"}
    upsert_row(
        conn, table="sales", row=row, primary_key="sale_id", allowed_tables=ALLOWED
    )
    results = query_db(conn, "SELECT * FROM sales WHERE region_id = ?", ["US-TX"])
    assert results == []
    close_db(conn)
