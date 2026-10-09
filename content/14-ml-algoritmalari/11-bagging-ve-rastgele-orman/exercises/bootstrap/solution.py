import numpy as np


def bootstrap(n, seed):
    rng = np.random.default_rng(seed)
    return rng.integers(0, n, n).tolist()

print(bootstrap(8, 0))
print(bootstrap(5, 1))
