"""Tests for datafun_streaming.data_validation.validation_utils."""

from datafun_streaming.data_validation.validation_utils import (
    add_validation_errors,
    validate_boolean_text,
    validate_datetime,
    validate_positive_integer,
    validate_required_fields,
)

# === validate_boolean_text ===


def test_validate_boolean_text_true() -> None:
    assert validate_boolean_text("true", field_name="is_member") == []


def test_validate_boolean_text_false() -> None:
    assert validate_boolean_text("false", field_name="is_member") == []


def test_validate_boolean_text_case_insensitive() -> None:
    assert validate_boolean_text("True", field_name="is_member") == []
    assert validate_boolean_text("FALSE", field_name="is_member") == []


def test_validate_boolean_text_invalid() -> None:
    errors = validate_boolean_text("yes", field_name="is_member")
    assert len(errors) == 1
    assert "is_member" in errors[0]


# === validate_datetime ===


def test_validate_datetime_valid_iso() -> None:
    assert validate_datetime("2026-05-08T12:00:00") == []


def test_validate_datetime_valid_utc_z() -> None:
    assert validate_datetime("2026-05-08T12:00:00Z") == []


def test_validate_datetime_invalid() -> None:
    errors = validate_datetime("not-a-date")
    assert len(errors) == 1
    assert "not-a-date" in errors[0]


# === validate_positive_integer ===


def test_validate_positive_integer_valid() -> None:
    assert validate_positive_integer("1") == []
    assert validate_positive_integer("100") == []


def test_validate_positive_integer_zero() -> None:
    errors = validate_positive_integer("0")
    assert len(errors) == 1


def test_validate_positive_integer_negative() -> None:
    errors = validate_positive_integer("-5")
    assert len(errors) == 1


def test_validate_positive_integer_not_a_number() -> None:
    errors = validate_positive_integer("abc")
    assert len(errors) == 1


# === validate_required_fields ===


def test_validate_required_fields_all_present() -> None:
    record = {"sale_id": "S001", "region_id": "US-MO"}
    assert (
        validate_required_fields(
            record=record, required_fields=["sale_id", "region_id"]
        )
        == []
    )


def test_validate_required_fields_missing_field() -> None:
    record = {"sale_id": "S001"}
    errors = validate_required_fields(
        record=record, required_fields=["sale_id", "region_id"]
    )
    assert len(errors) == 1
    assert "region_id" in errors[0]


def test_validate_required_fields_blank_field() -> None:
    record = {"sale_id": "S001", "region_id": "   "}
    errors = validate_required_fields(
        record=record, required_fields=["sale_id", "region_id"]
    )
    assert len(errors) == 1
    assert "region_id" in errors[0]


def test_validate_required_fields_empty_required_list() -> None:
    record = {"sale_id": "S001"}
    assert validate_required_fields(record=record, required_fields=[]) == []


# === add_validation_errors ===


def test_add_validation_errors_attaches_errors() -> None:
    record = {"sale_id": "S001"}
    result = add_validation_errors(record=record, errors=["Missing field: region_id"])
    assert "validation_errors" in result
    assert "Missing field: region_id" in result["validation_errors"]


def test_add_validation_errors_does_not_mutate_original() -> None:
    record = {"sale_id": "S001"}
    add_validation_errors(record=record, errors=["error"])
    assert "validation_errors" not in record


def test_add_validation_errors_joins_multiple() -> None:
    record = {"sale_id": "S001"}
    result = add_validation_errors(record=record, errors=["err1", "err2"])
    assert "err1" in result["validation_errors"]
    assert "err2" in result["validation_errors"]
