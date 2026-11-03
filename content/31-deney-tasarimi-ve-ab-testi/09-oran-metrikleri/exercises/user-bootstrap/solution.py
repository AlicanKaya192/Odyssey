import numpy as np


def boot_ratio_se(x, y, reps=1000, seed=0):
    rng = np.random.default_rng(seed)
    x, y = np.asarray(x), np.asarray(y)
    ratios = []
    for _ in range(reps):
        i = rng.integers(0, len(x), len(x))
        ratios.append(y[i].sum() / x[i].sum())
    return round(float(np.std(ratios)), 4)


print(boot_ratio_se([3, 5, 2, 8, 6, 4, 9, 1], [1, 2, 0, 3, 2, 1, 4, 0]))
