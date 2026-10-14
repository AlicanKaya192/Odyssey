import numpy as np


def bootstrap(a, b, n, seed):
    a, b = np.array(a), np.array(b)
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n):
        pick = rng.integers(0, len(a), len(a))
        diffs.append(a[pick].sum() - b[pick].sum())
    low, high = np.percentile(diffs, [5, 95])
    return [int(a.sum() - b.sum()), round(float(low), 1), round(float(high), 1)]


a = [1, 1, 0, 1, 1, 0, 1, 1]
b = [1, 0, 0, 1, 1, 0, 1, 0]
print(bootstrap(a, b, 2000, 0))
