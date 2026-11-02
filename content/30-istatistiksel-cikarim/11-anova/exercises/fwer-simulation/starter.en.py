import itertools
import numpy as np
from scipy import stats


def fwer(k, n, reps, seed):
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        groups = rng.normal(0, 1, size=(k, n))
        hits += stats.ttest_ind(groups[0], groups[1]).pvalue < 0.05
    return round(hits / reps, 3)


print(fwer(4, 50, 800, 0))
print(fwer(2, 50, 800, 0))
