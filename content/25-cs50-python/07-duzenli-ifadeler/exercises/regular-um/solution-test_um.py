from um import count


def test_one():
    assert count("um") == 1
    assert count("hello, um, world") == 1


def test_case():
    assert count("Um, thanks, UM...") == 2


def test_inside_words():
    assert count("yummy") == 0
    assert count("umbrella") == 0
    assert count("Um, thanks for the album.") == 1
