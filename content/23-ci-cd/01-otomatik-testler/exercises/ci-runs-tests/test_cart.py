from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60


def test_total_with_discount():
    assert cart_total([50, 50], discount=20) == 80


def test_empty_cart():
    assert cart_total([]) == 0
