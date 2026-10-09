import math


def almost_equal(a, b):
    # math.isclose(..., abs_tol=1e-9)
    return a == b

print(almost_equal(0.1 + 0.2, 0.3))
print(almost_equal(1e-10, 0))
print(almost_equal(1.0, 1.1))
