import math


def prefer_prob(r_a, r_b):
    return round(1 / (1 + math.exp(-(r_a - r_b))), 3)


print(prefer_prob(2.0, 1.0))
print(prefer_prob(0.0, 0.0))
