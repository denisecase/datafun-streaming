"""Tests for datafun_streaming.data_validation.types."""

from dataclasses import FrozenInstanceError

import pytest

from datafun_streaming.data_validation.types import (
    AllowedValuesSet,
    ErrorMessages,
    ValidationResult,
)


def test_validation_result_valid() -> None:
    result = ValidationResult(is_valid=True, errors=[])
    assert result.is_valid is True
    assert result.errors == []


def test_validation_result_invalid() -> None:
    result = ValidationResult(is_valid=False, errors=["Missing field: region_id"])
    assert result.is_valid is False
    assert len(result.errors) == 1


def test_validation_result_is_frozen() -> None:
    result = ValidationResult(is_valid=True, errors=[])

    with pytest.raises(FrozenInstanceError):
        result.is_valid = False  # type: ignore[misc]


def test_error_messages_is_list() -> None:
    errors: ErrorMessages = ["err1", "err2"]
    assert isinstance(errors, list)


def test_allowed_values_set_is_set() -> None:
    allowed: AllowedValuesSet = {"US-MO", "US-KS"}
    assert isinstance(allowed, set)
    assert "US-MO" in allowed
