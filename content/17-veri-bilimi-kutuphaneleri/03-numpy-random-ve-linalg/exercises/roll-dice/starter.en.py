import numpy as np


def roll(seed, n):
    np.random.seed(seed)
    return np.random.randint(1, 7, size=n).tolist()

print(roll(42, 5), roll(42, 5) == roll(42, 5))
