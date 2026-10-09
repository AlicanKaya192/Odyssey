import random


def estimate_area(n, seed):
    rng = random.Random(seed)
    below = 0
    # n points: x first, then y.
    return round(below / n, 4)

for n in (100, 10_000, 1_000_000):
    print(n, estimate_area(n, 7))
