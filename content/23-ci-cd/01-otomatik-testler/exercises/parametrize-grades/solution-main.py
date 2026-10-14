import pytest

from grades import letter


@pytest.mark.parametrize("score, expected", [
    (90, "A"),
    (89, "B"),
    (80, "B"),
    (79, "C"),
    (70, "C"),
    (69, "F"),
])
def test_letter(score, expected):
    assert letter(score) == expected
