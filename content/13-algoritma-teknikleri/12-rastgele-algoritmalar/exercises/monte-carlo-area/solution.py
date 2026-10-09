import random


def estimate_area(n, seed):
    rng = random.Random(seed)
    below = 0
    for _ in range(n):
        x = rng.random()
        y = rng.random()
        if y <= x * x:
            below += 1
    return round(below / n, 4)

for n in (100, 10_000, 1_000_000):
    print(n, estimate_area(n, 7))
