from plates import is_valid


def test_length():
    assert is_valid("CS") == True
    assert is_valid("H") == False
    assert is_valid("OUTATIME") == False


def test_start():
    assert is_valid("CS50") == True
    assert is_valid("50CS") == False
    assert is_valid("C50") == False


def test_numbers():
    assert is_valid("AAA222") == True
    assert is_valid("AAA22A") == False
    assert is_valid("CS05") == False


def test_punctuation():
    assert is_valid("CS 50") == False
    assert is_valid("PI3.14") == False
