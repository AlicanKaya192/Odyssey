import math


def needed_n(sigma, target):
    return math.ceil(sigma / target)


print(needed_n(6.13, 0.5))
print(needed_n(120, 10))
