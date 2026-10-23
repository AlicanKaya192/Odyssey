from leap import is_leap


def test_divisible_by_4():
    assert is_leap(2024) == True
    assert is_leap(2023) == False


def test_century():
    assert is_leap(1900) == False


def test_divisible_by_400():
    assert is_leap(2000) == True
