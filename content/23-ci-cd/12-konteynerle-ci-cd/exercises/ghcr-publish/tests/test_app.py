from app import greet


def test_greet():
    assert greet("Ada") == "Hello, Ada!"
