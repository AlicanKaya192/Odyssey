import pytest

from ages import parse_age


def test_valid_age():
    assert parse_age("42") == 42


def test_text_is_rejected():
    with pytest.raises(ValueError):
        parse_age("abc")


def test_negative_is_rejected():
    with pytest.raises(ValueError):
        parse_age("-1")


def test_too_old_is_rejected():
    with pytest.raises(ValueError):
        parse_age("200")
