import numpy as np


def roll(seed, n):
    rng = np.random.default_rng(seed)
    return rng.integers(1, 7, size=n).tolist()

print(roll(42, 5), roll(42, 5) == roll(42, 5))
