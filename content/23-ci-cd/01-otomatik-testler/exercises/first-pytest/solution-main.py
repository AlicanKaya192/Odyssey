from shipping import shipping_cost


def test_one_kilo():
    assert shipping_cost(1) == 5


def test_five_kilos():
    assert shipping_cost(5) == 9


def test_seven_kilos():
    assert shipping_cost(7) == 13
