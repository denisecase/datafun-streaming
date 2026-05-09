"""io/errors.py."""


# === EXPORTS ===

__all__ = [
    "missing_csv_file_message",
    "missing_csv_field_message",
]

# === DEFINE HELPER FUNCTIONS ===


def missing_csv_file_message(*, path: str) -> str:
    """Return help text for a missing CSV file.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        path: The file path that was not found.

    Returns:
        A help message with troubleshooting steps.
    """
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
This project needs a CSV file to generate messages.
Required CSV file not found:
    {path}

CHECK:
1. Confirm you are running the command from the project root folder.
2. Confirm the data folder exists.
3. Confirm data/sales.csv exists.
4. If the file was deleted, restore it from the repository.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()


def missing_csv_field_message(*, field: str, available_fields: list[str]) -> str:
    """Return help text for a missing CSV field.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        field: The name of the missing field.
        available_fields: A list of field names that were found in the CSV file.

    Returns:
        A help message with troubleshooting steps.
    """
    fields = ", ".join(available_fields)

    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
The project read the CSV file,
but an expected column was not present.
Required CSV field missing:
    {field}

Available fields were:
    {fields}

CHECK:
1. Open data/sales.csv.
2. Confirm the header row includes: {field}
3. Header names must match exactly.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()
