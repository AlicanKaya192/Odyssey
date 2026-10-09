import math


def ways(n, k, ordered):
    if ordered:
        return math.perm(n, k)
    return math.comb(n, k)

print(ways(10, 3, False))
print(ways(10, 3, True))
