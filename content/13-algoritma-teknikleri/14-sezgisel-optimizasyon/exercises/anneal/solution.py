import math
import random


def f(x):
    return x * x / 10 + 10 * math.sin(x)


def anneal(x, seed):
    rng = random.Random(seed)
    temp = 20.0
    best = x
    for _ in range(3000):
        cand = x + rng.uniform(-3, 3)
        delta = f(cand) - f(x)
        if delta < 0 or rng.random() < math.exp(-delta / temp):
            x = cand
        if f(x) < f(best):
            best = x
        temp *= 0.998
    return round(best, 2)

for seed in range(4):
    print(seed, anneal(25.0, seed))
