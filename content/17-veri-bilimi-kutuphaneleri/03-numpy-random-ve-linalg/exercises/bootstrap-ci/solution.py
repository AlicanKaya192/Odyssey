import numpy as np


def bootstrap_ci(values, n, seed):
    rng = np.random.default_rng(seed)
    data = np.array(values, dtype=float)
    samples = rng.choice(data, size=(n, data.size), replace=True)
    low, high = np.percentile(samples.mean(axis=1), [2.5, 97.5])
    return [round(float(low), 1), round(float(high), 1)]

print(bootstrap_ci([10, 12, 9, 14, 11, 13, 10, 15], 2000, 3))
