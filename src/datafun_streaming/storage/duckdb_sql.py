"""src/datafun_streaming/storage/duckdb_sql.py.

Pure SQL string builders for DuckDB streaming tables.

These functions build SQL statements as strings.
They require no database connection and have no side effects.
All use module-level constant table names, never raw user input.

Author: Denise Case
Date: 2026-05
"""

# === EXPORTS ===

__all__ = [
    "build_create_table_sql",
    "build_clear_table_sql",
    "build_insert_sql",
]


# === DEFINE SQL BUILDER FUNCTIONS ===


def build_create_table_sql(table_name: str, fieldnames: list[str]) -> str:
    """Build a DuckDB CREATE TABLE IF NOT EXISTS statement.

    All columns are declared as VARCHAR.
    Use this to initialize tables before writing records.

    Arguments:
        table_name: The table to create.
        fieldnames: The field names to include as VARCHAR columns.

    Returns:
        A CREATE TABLE IF NOT EXISTS SQL string.

    Example:
        sql = build_create_table_sql("sales", ["order_id", "region_id"])
        connection.execute(sql)
    """
    columns = ", ".join(f"{field} VARCHAR" for field in fieldnames)
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"  # noqa: S608 - caller responsible for validated table name


def build_clear_table_sql(table_name: str) -> str:
    """Build a DuckDB DELETE statement to clear all rows from a table.

    Use this at the start of a consumer run to reset the table.

    Arguments:
        table_name: The table to clear.

    Returns:
        A DELETE FROM SQL string.

    Example:
        sql = build_clear_table_sql("sales")
        connection.execute(sql)
    """
    return f"DELETE FROM {table_name}"  # noqa: S608 - caller responsible for validated table name


def build_insert_sql(table_name: str, fieldnames: list[str]) -> str:
    """Build a DuckDB INSERT statement with ? parameter placeholders.

    The returned SQL expects one ? per field, passed as a list of values
    to connection.execute().

    Arguments:
        table_name: The table to insert into.
        fieldnames: The field names to insert.

    Returns:
        An INSERT INTO SQL string with ? placeholders.

    Example:
        sql = build_insert_sql("sales", ["order_id", "region_id"])
        connection.execute(sql, ["S001", "US-MO"])
    """
    columns = ", ".join(fieldnames)
    placeholders = ", ".join("?" for _ in fieldnames)
    return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"  # noqa: S608 - caller responsible for validated table name
