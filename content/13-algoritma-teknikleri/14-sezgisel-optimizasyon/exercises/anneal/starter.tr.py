import math
import random


def f(x):
    return x * x / 10 + 10 * math.sin(x)


def anneal(x, seed):
    rng = random.Random(seed)
    temp = 20.0
    best = x
    # 3000 adim: aday, kabul, en iyi, sogut.
    return round(best, 2)

for seed in range(4):
    print(seed, anneal(25.0, seed))
