from numb3rs import validate


def test_valid():
    assert validate("127.0.0.1") is True
    assert validate("255.255.255.255") is True
    assert validate("0.0.0.0") is True


def test_range():
    assert validate("256.1.1.1") is False
    assert validate("1.256.1.1") is False
    assert validate("1.1.256.1") is False
    assert validate("1.1.1.256") is False


def test_format():
    assert validate("1.2.3") is False
    assert validate("1.2.3.4.5") is False
    assert validate("cat") is False
    assert validate("1.2.3.-4") is False
