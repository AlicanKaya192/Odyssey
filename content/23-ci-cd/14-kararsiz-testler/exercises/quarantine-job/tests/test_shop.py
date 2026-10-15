import random

import pytest

from shop import total


def test_total():
    assert total([1.5, 2.25]) == 3.75


@pytest.mark.flaky
def test_total_random():
    assert random.random() < 0.9
