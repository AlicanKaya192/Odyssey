from tempconv.convert import c_to_f


def test_freezing():
    assert c_to_f(0) == 32
