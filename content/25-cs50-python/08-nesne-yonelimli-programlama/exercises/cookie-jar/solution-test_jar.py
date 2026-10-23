import pytest

from jar import COOKIE, Jar


def test_init():
    jar = Jar()
    assert jar.capacity == 12
    assert jar.size == 0
    assert Jar(3).capacity == 3
    with pytest.raises(ValueError):
        Jar(-1)


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(3)
    assert str(jar) == COOKIE * 3


def test_deposit():
    jar = Jar(5)
    jar.deposit(2)
    jar.deposit(3)
    assert jar.size == 5
    with pytest.raises(ValueError):
        jar.deposit(1)


def test_withdraw():
    jar = Jar()
    jar.deposit(4)
    jar.withdraw(3)
    assert jar.size == 1
    with pytest.raises(ValueError):
        jar.withdraw(2)
