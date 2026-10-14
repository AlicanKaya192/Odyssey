import numpy as np


def rejection_stats(n, seed):
    r = np.random.default_rng(seed)
    x = r.random(n)
    height = r.random(n) * 1.5
    kept = x[height < 6 * x * (1 - x)]
    return [round(len(kept) / n, 3), round(float(kept.mean()), 3)]


print(rejection_stats(10000, 2))
print(rejection_stats(500, 8))
