"""src/datafun_streaming/storage/duckdb_utils.py.

DuckDB utilities for streaming data.

Provides functions to initialize, write to, query, and close
a DuckDB database from a streaming consumer.

This is domain-agnostic: it works with any table name and any row dict.
Tables are created automatically from the first row received.
Schema is inferred from Python value types.

Author: Denise Case
Date: 2026-05
"""

# === IMPORTS ===

import logging
from pathlib import Path
from typing import Any

import duckdb

# === DECLARE EXPORTS

__all__ = [
    "connect_to_database",
    "init_db",
    "close_db",
    "upsert_row",
    "query_db",
    "safe_table_name",
]

# === CONFIGURE LOGGER ===

LOG = logging.getLogger(__name__)

# === TYPE MAP: Python types to DuckDB column types ===

_DUCKDB_TYPE_MAP: dict[type, str] = {
    str: "VARCHAR",
    int: "INTEGER",
    float: "DOUBLE",
    bool: "BOOLEAN",
}

# === DEFINE FUNCTIONS ===


def connect_to_database(database_file_path: Path) -> duckdb.DuckDBPyConnection:
    """Connect to the DuckDB database file.

    Arguments:
        database_file_path: Path to the DuckDB database file.

    Returns:
        An open DuckDB connection.
    """
    return duckdb.connect(str(database_file_path))


def close_db(conn: duckdb.DuckDBPyConnection) -> None:
    """Close a DuckDB connection.

    Arguments:
        conn: An open DuckDB connection.

    Returns:
        None.
    """
    conn.close()
    LOG.debug("DuckDB connection closed.")


def init_db(path: Path) -> duckdb.DuckDBPyConnection:
    """Open or create a DuckDB database at the given path.

    If the file already exists it is opened and reused.
    If it does not exist it is created.

    Arguments:
        path: File path for the DuckDB database (e.g. data/output/sales.duckdb).

    Returns:
        An open DuckDB connection.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(path))
    LOG.debug(f"DuckDB opened: {path}")
    return conn


def safe_table_name(table_name: str, allowed: frozenset[str]) -> str:
    """Return table_name after confirming it is in the allowed list.

    SQL identifiers (table names, column names) cannot use parameterized
    query placeholders. This allowlist check prevents accidental injection
    if a caller passes an unexpected string.

    Arguments:
        table_name: The table name to validate.
        allowed: A frozenset of allowed table names.

    Returns:
        The validated table name, unchanged.

    Raises:
        ValueError: If table_name is not in the allowed list.
    """
    if table_name not in allowed:
        raise ValueError(
            f"Table name {table_name!r} is not in the allowed list. "
            f"Allowed: {sorted(allowed)}"
        )
    return table_name


def query_db(
    conn: duckdb.DuckDBPyConnection,
    sql: str,
    params: list[Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a SQL query and return results as a list of dicts.

    Arguments:
        conn:   Open DuckDB connection.
        sql:    SQL query string. Use ? for parameter placeholders.
        params: Optional list of parameter values for placeholders.

    Returns:
        A list of row dicts. Empty list if no rows matched.

    Example:
        rows = query_db(conn, "SELECT * FROM sales WHERE region_id = ?", ["US-MO"])
    """
    result = conn.execute(sql, params or [])
    columns = [desc[0] for desc in result.description]
    return [dict(zip(columns, row, strict=False)) for row in result.fetchall()]


def upsert_row(
    conn: duckdb.DuckDBPyConnection,
    *,
    table: str,
    row: dict[str, Any],
    primary_key: str,
    allowed_tables: frozenset[str],  # ← caller provides this
) -> None:
    """Insert or replace one row in a DuckDB table.

    All arguments after the asterisk must be passed as keyword arguments.

    Creates the table on the first call if it does not exist.
    On subsequent calls with the same primary key value,
    the existing row is replaced with the new values.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        conn:        Open DuckDB connection.
        table:       Table name to write to.
        row:         The row to insert or replace.
        primary_key: The field name that uniquely identifies each row.
        allowed_tables: A frozenset of allowed table names.

    Returns:
        None.
    """
    # Validate before use: table name must be in the allowlist,
    # primary key must be a field in the row.
    safe = safe_table_name(table, allowed_tables)
    safe_pk = safe_table_name(primary_key, frozenset(row.keys()))

    # Pass the validated names so _ensure_table never receives raw input.
    _ensure_table(conn, safe, row, safe_pk)

    pk_value = row[safe_pk]
    conn.execute(
        f"DELETE FROM {safe} WHERE {safe_pk} = ?",  # noqa: S608 - identifiers validated via safe_table_name allowlist
        [pk_value],
    )

    cols = ", ".join(row.keys())
    placeholders = ", ".join(["?"] * len(row))
    conn.execute(
        f"INSERT INTO {safe} ({cols}) VALUES ({placeholders})",  # noqa: S608 - identifiers validated via safe_table_name allowlist
        list(row.values()),
    )
    LOG.debug(f"Upserted row into {safe} with primary key {safe_pk}={pk_value}")


# == DEFINE INTERNAL HELPER FUNCTIONS (not exported) ===


def _ensure_table(
    conn: duckdb.DuckDBPyConnection,
    table: str,
    row: dict[str, Any],
    primary_key: str,
) -> None:
    """Create the table if it does not already exist.

    Infers column types from the Python types of the row values.
    The primary key column is marked as PRIMARY KEY.

    Arguments:
        conn:        Open DuckDB connection.
        table:       Table name to create.
        row:         A representative row dict used for schema inference.
        primary_key: The field name to use as the primary key.

    Returns:
        None.
    """
    columns = []
    for col, val in row.items():
        col_type = _infer_column_type(val)
        if col == primary_key:
            columns.append(f"{col} {col_type} PRIMARY KEY")
        else:
            columns.append(f"{col} {col_type}")

    col_defs = ", ".join(columns)
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({col_defs})")  # noqa: S608 - identifiers validated via safe_table_name allowlist


def _infer_column_type(value: Any) -> str:
    """Infer a DuckDB column type from a Python value.

    Arguments:
        value: A Python value whose type will be inspected.

    Returns:
        A DuckDB type string (e.g. "VARCHAR", "DOUBLE").
    """
    return _DUCKDB_TYPE_MAP.get(type(value), "VARCHAR")
