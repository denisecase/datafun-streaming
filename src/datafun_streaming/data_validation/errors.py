"""data_validation/errors.py.

Error messages for validation.
"""


def reference_validation_failed_message(*, label: str, error_count: int) -> str:
    """Return help text when a reference data file fails validation."""
    return f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
A reference data file failed validation.
File:   {label}
Errors: {error_count} problem(s) found.

The producer cannot run until all reference files are valid.
Fix the reference file before retrying.

CHECK:
1. Open data/{label} and inspect the header row.
2. Confirm all required fields are present and spelled correctly.
3. Confirm no rows have blank values in required fields.
4. See data_contract_case.py for the list of required fields.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""".strip()
