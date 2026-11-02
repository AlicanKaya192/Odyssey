import numpy as np


def average_miss(values, n, repeats):
    values = np.array(values, dtype=float)
    true_mean = values.mean()
    misses = []
    for seed in range(repeats):
        rng = np.random.default_rng(seed)
        sample = rng.choice(values, size=n, replace=False)
        misses.append(abs(sample.mean() - true_mean))
    return round(float(np.mean(misses)), 3)


values = list(range(1, 101))
print(average_miss(values, 4, 500))
print(average_miss(values, 16, 500))
print(average_miss(values, 64, 500))
