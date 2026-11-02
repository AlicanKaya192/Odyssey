import itertools
import numpy as np
from scipy import stats


def fwer(k, n, reps, seed):
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(reps):
        groups = rng.normal(0, 1, size=(k, n))
        pairs = itertools.combinations(range(k), 2)
        p = [stats.ttest_ind(groups[i], groups[j]).pvalue for i, j in pairs]
        hits += min(p) < 0.05
    return round(hits / reps, 3)


print(fwer(4, 50, 800, 0))
print(fwer(2, 50, 800, 0))
