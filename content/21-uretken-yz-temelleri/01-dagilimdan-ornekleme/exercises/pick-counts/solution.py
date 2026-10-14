import numpy as np


def pick_counts(probs, n, seed):
    cum = np.cumsum(probs)
    u = np.random.default_rng(seed).random(n)
    picks = np.searchsorted(cum, u, side="right")
    return np.bincount(picks, minlength=len(probs)).tolist()


print(pick_counts([0.5, 0.3, 0.2], 1000, 4))
print(pick_counts([0.9, 0.1], 50, 1))
