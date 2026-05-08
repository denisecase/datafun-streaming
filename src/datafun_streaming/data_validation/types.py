"""src/datafun_streaming/data_validation/types.py.

Type aliases and dataclasses for validation results.

Import from here whenever you need to type-hint a record or validation result.
"""

# === IMPORTS ===

from dataclasses import dataclass

from datafun_streaming.core.types import DataRecordDict, DataRecordDictList

# === EXPORTS ===

__all__ = [
    "DataRecordDict",
    "DataRecordDictList",
    "ErrorMessage",
    "ErrorMessages",
    "AllowedValuesSet",
    "ValidationResult",
]

# === TYPE ALIASES ===

ErrorMessage = str
ErrorMessages = list[ErrorMessage]
AllowedValuesSet = set[str]


@dataclass(frozen=True)
class ValidationResult:
    """Result from checking one record against the data contract.

    Attributes:
        is_valid: True if the record passed all validation checks.
        errors: List of error messages; empty when is_valid is True.
    """

    is_valid: bool
    errors: ErrorMessages
