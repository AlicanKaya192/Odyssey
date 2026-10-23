import pytest

from seasons import minutes_between, sing


def test_minutes_between():
    assert minutes_between("1999-01-01", "2000-01-01") == 525600
    assert minutes_between("2000-01-01", "2001-01-01") == 527040
    assert minutes_between("1998-06-20", "2000-06-20") == 1052640


def test_invalid_date():
    with pytest.raises(ValueError):
        minutes_between("January 1, 1999", "2000-01-01")
    with pytest.raises(ValueError):
        minutes_between("1999-02-30", "2000-01-01")


def test_sing():
    assert sing(525600) == "Five hundred twenty-five thousand, six hundred minutes"
    assert sing(527040) == "Five hundred twenty-seven thousand forty minutes"
    assert sing(1051200) == "One million, fifty-one thousand, two hundred minutes"
