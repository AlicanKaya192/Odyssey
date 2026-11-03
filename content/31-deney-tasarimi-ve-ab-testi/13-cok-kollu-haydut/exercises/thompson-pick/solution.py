import numpy as np


def thompson_pick(k, n, seed=0):
    rng = np.random.default_rng(seed)
    k, n = np.asarray(k), np.asarray(n)
    return int(np.argmax(rng.beta(1 + k, 1 + n - k)))


print(thompson_pick([1, 0], [10, 1]))
