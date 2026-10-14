from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60
