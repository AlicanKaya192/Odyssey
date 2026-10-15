import pytest

from tempconv.convert import c_to_f, f_to_c

CASES = [(0, 32), (100, 212), (-40, -40), (37, 98.6)]


@pytest.mark.parametrize("celsius, fahrenheit", CASES)
def test_c_to_f(celsius, fahrenheit):
    assert c_to_f(celsius) == fahrenheit


def test_round_trip():
    assert f_to_c(c_to_f(21.5)) == 21.5
