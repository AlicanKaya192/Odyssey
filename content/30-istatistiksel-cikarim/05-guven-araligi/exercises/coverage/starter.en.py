import numpy as np
from scipy import stats


def coverage(values, n, reps, seed, level):
    values = np.array(values, dtype=float)
    true_mean = values.mean()
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(reps, n))
    means = samples.mean(axis=1)
    ses = samples.std(axis=1, ddof=1) / np.sqrt(n)
    mult = 1.96
    hit = np.abs(means - true_mean) <= mult * ses
    return round(float(hit.mean()), 3)


data = list(range(1, 51))
print(coverage(data, 5, 3000, 0, 0.95))
print(coverage(data, 30, 3000, 0, 0.90))
