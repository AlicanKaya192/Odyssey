import numpy as np
from scipy import stats


def skew_of_means(values, n, reps, seed):
    rng = np.random.default_rng(seed)
    means = rng.choice(values, size=(reps, n)).mean(axis=1)
    return round(float(stats.skew(means)), 2)


data = [1, 1, 1, 1, 2, 2, 3, 5, 10, 40]
print(skew_of_means(data, 2, 4000, 0))
print(skew_of_means(data, 50, 4000, 0))
