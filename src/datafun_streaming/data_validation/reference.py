"""src/datafun_streaming/data_validation/reference.py.

Reference data validation helpers.

Provides functions for working with lookup tables:
building lookup sets from CSV rows and validating reference records.
"""

# === IMPORTS ===

from datafun_streaming.core.types import DataRecordDictList
from datafun_streaming.data_validation.types import AllowedValuesSet
from datafun_streaming.data_validation.validation_utils import validate_required_fields

# === EXPORTS ===

__all__ = [
    "make_lookup_set",
    "validate_reference_records",
]


def make_lookup_set(records: DataRecordDictList, key_field: str) -> AllowedValuesSet:
    """Create a set of allowed values for a field in a reference table.

    Arguments:
        records: A list of row dictionaries from a reference CSV file.
        key_field: The field to use as the key for allowed values.

    Returns:
        A set of allowed values for the specified key field.
    """
    values: AllowedValuesSet = set()
    for record in records:
        value: str = record.get(key_field, "").strip()
        if value:
            values.add(value)
    return values


def validate_reference_records(
    *,
    records: DataRecordDictList,
    required_fields: list[str],
    label: str,
) -> list[str]:
    """Validate reference records and return file-level errors.

    Arguments:
        records: Reference data records to validate.
        required_fields: Field names required in each record.
        label: Label for this reference file, used in error messages.

    Returns:
        A list of errors, or an empty list if all records are valid.
    """
    errors: list[str] = []
    for record_number, record in enumerate(records, start=1):
        for error in validate_required_fields(
            record=record, required_fields=required_fields
        ):
            errors.append(f"{label} record {record_number}: {error}")
    return errors
