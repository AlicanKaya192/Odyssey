import numpy as np


def thompson_pick(k, n, seed=0):
    k, n = np.asarray(k), np.asarray(n)
    return int(np.argmax(k / n))


print(thompson_pick([1, 0], [10, 1]))
