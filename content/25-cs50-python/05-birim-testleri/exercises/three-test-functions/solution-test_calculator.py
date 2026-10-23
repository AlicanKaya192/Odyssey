from calculator import cube


def test_positive():
    assert cube(2) == 8
    assert cube(3) == 27


def test_negative():
    assert cube(-2) == -8
    assert cube(-3) == -27


def test_zero():
    assert cube(0) == 0
