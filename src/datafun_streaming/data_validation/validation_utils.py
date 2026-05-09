"""src/datafun_streaming/data_validation/validation_utils.py.

Generic field-level validation functions.

Each function checks one thing about one value and returns a list of
error strings, empty if valid, one or more messages if not.
These functions know nothing about domains, reference data, or business rules.
They only check types, formats, and value ranges.

OBS:
  Add functions to this file as validation requirements evolve.
"""

# == IMPORTS ==

from datetime import datetime

from datafun_streaming.core.types import DataRecordDict
from datafun_streaming.data_validation.types import ErrorMessages

# == EXPORTS ==

__all__ = [
    "add_validation_errors",
    "validate_boolean_text",
    "validate_datetime",
    "validate_positive_integer",
    "validate_required_fields",
]


def add_validation_errors(
    *,
    record: DataRecordDict,
    errors: ErrorMessages,
) -> DataRecordDict:
    """Return a copy of a record with validation errors attached.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        record: A dictionary representing one data record.
        errors: A list of validation error messages.

    Returns:
        A copy of the record with a validation_errors field appended.
    """
    output = dict(record)
    output["validation_errors"] = " | ".join(errors)
    return output


def validate_boolean_text(value: str, *, field_name: str) -> list[str]:
    """Return errors for an invalid boolean text value.

    All boolean values must be represented as
    "true" or "false" (case-insensitive).

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        value: The text value to validate.
        field_name: The name of the field being validated, for error messages.

    Returns:
        A list of errors, or an empty list if the value is valid.
    """
    allowed_values = {"true", "false"}

    if value.lower() not in allowed_values:
        return [f"{field_name} must be true or false: {value}"]

    return []


def validate_datetime(value: str) -> list[str]:
    """Return errors for an invalid datetime value.

    All datetime values must be in ISO 8601 format.

    Arguments:
        value: The text value to validate.

    Returns:
        A list of errors, or an empty list if the value is valid.
    """
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return [f"Invalid datetime: {value}"]

    return []


def validate_positive_integer(value: str) -> list[str]:
    """Return errors for an invalid positive integer value.

    All positive integer values must be integers greater than or equal to 1.

    Arguments:
        value: The text value to validate.

    Returns:
        A list of errors, or an empty list if the value is valid.
    """
    try:
        number = int(value)
    except ValueError:
        return [f"Value must be an integer: {value}"]

    if number < 1:
        return [f"Value must be at least 1: {value}"]

    return []


# === DEFINE FIELD VALIDATION HELPERS ===


def validate_required_fields(
    *,
    record: DataRecordDict,
    required_fields: list[str],
) -> list[str]:
    """Return errors for missing or blank required fields.

    All required fields must be present and not blank.

    All arguments after the asterisk must be passed as keyword arguments.

    Arguments:
        record: A dictionary representing one data record / row.
        required_fields: A list of field names that are required.

    Returns:
        A list of errors, or
        an empty list if all required fields are present.
    """
    errors: list[str] = []

    for field_name in required_fields:
        if field_name not in record:
            errors.append(f"Missing required field: {field_name}")
        elif not record[field_name].strip():
            errors.append(f"Required field is blank: {field_name}")

    return errors
