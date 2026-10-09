import numpy as np


def permutation_p(a, b, rounds, seed):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    real = abs(a.mean() - b.mean())
    both = np.concatenate([a, b])
    rng = np.random.default_rng(seed)
    # rounds kez karistir, farki hesapla, say.
    return 1.0

a = [12.1, 11.8, 12.6, 13.0, 12.4]
b = [11.2, 11.5, 11.0, 11.9, 11.4]
print(permutation_p(a, b, 999, 0))
print(permutation_p([1, 2, 3], [1, 2, 3], 99, 0))
