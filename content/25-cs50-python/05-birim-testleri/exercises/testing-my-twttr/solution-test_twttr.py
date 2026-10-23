from twttr import shorten


def test_lowercase():
    assert shorten("twitter") == "twttr"


def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"
    assert shorten("Twitter") == "Twttr"


def test_numbers():
    assert shorten("CS50") == "CS50"


def test_punctuation():
    assert shorten("What's your name?") == "Wht's yr nm?"
