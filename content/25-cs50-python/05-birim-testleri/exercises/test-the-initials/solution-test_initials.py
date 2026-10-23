from initials import initials


def test_two_words():
    assert initials("David Malan") == "DM"


def test_lowercase():
    assert initials("ada lovelace") == "AL"


def test_one_word():
    assert initials("Cher") == "C"
