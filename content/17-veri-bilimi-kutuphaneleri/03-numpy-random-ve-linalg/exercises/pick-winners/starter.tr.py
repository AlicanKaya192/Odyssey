import numpy as np


def pick(ids, k, seed):
    rng = np.random.default_rng(seed)
    return rng.choice(ids, size=k).tolist()

print(pick(list(range(100, 110)), 4, 0))
