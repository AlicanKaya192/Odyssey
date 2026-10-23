import pytest

from fuel import convert, gauge


def test_convert():
    assert convert("1/4") == 25
    assert convert("3/4") == 75
    assert convert("2/3") == 67


def test_convert_errors():
    with pytest.raises(ValueError):
        convert("5/4")
    with pytest.raises(ValueError):
        convert("cat/dog")
    with pytest.raises(ZeroDivisionError):
        convert("1/0")


def test_gauge():
    assert gauge(1) == "E"
    assert gauge(0) == "E"
    assert gauge(99) == "F"
    assert gauge(100) == "F"
    assert gauge(50) == "50%"
    assert gauge(2) == "2%"
