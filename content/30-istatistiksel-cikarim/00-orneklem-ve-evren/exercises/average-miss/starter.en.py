import numpy as np


def average_miss(values, n, repeats):
    values = np.array(values, dtype=float)
    true_mean = values.mean()
    rng = np.random.default_rng(0)
    sample = rng.choice(values, size=n, replace=False)
    return round(float(abs(sample.mean() - true_mean)), 3)


values = list(range(1, 101))
print(average_miss(values, 4, 500))
print(average_miss(values, 16, 500))
print(average_miss(values, 64, 500))
