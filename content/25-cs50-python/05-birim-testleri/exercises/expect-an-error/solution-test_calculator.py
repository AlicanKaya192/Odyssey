import pytest

from calculator import square


def test_numbers():
    assert square(2) == 4
    assert square(-3) == 9
    assert square(0) == 0


def test_str():
    with pytest.raises(TypeError):
        square("cat")
