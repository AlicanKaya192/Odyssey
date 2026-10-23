from validate import is_valid


def test_valid():
    assert is_valid("AB-1234")
    assert is_valid("ZZ-9000")


def test_letters():
    assert not is_valid("ab-1234")
    assert not is_valid("A-1234")
    assert not is_valid("ABC-1234")


def test_digits():
    assert not is_valid("AB-0123")
    assert not is_valid("AB-123")
    assert not is_valid("AB-12345")


def test_format():
    assert not is_valid("AB1234")
    assert not is_valid("XAB-1234")
    assert not is_valid("AB-1234 ")
