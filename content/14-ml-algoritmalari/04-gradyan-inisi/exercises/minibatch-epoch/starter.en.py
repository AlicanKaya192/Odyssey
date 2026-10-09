import numpy as np


def minibatch_epoch(A, y, w, lr, batch, seed):
    A, y, w = np.array(A, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    order = np.random.default_rng(seed).permutation(len(y))
    # Groups and steps.
    return w.round(4).tolist()

A = [[1, x] for x in range(10)]
y = [2 + 3 * x for x in range(10)]
w = [0.0, 0.0]
for epoch in range(3):
    w = minibatch_epoch(A, y, w, 0.01, 4, epoch)
    print(w)
