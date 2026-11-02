import numpy as np


def boot_mean_ci(values, reps=1000, seed=0):
    rng = np.random.default_rng(seed)
    values = np.asarray(values, dtype=float)
    means = [rng.choice(values, len(values), replace=False).mean()
             for _ in range(reps)]
    low, high = np.percentile(means, [2.5, 97.5])
    return [round(float(low), 2), round(float(high), 2)]


print(boot_mean_ci([12, 15, 9, 30, 14, 11, 13, 50, 10, 12]))
