import numpy as np
from scipy import stats
from ab_data import make_pageviews


def group_ratio(t):
    x = t["pageviews"].to_numpy(dtype=float)
    y = t["clicks"].to_numpy(dtype=float)
    r = y.mean() / x.mean()
    var = (y.var(ddof=1) - 2 * r * np.cov(x, y)[0, 1]
           + r ** 2 * x.var(ddof=1)) / (len(x) * x.mean() ** 2)
    return r, var, y.sum(), x.sum()

test = make_pageviews(n=20000, seed=31, lift=0.08)
ra, va, _, _ = group_ratio(test[test["group"] == "A"])
rb, vb, _, _ = group_ratio(test[test["group"] == "B"])
z = (rb - ra) / np.sqrt(va + vb)
print(round(float(ra), 4), round(float(rb), 4))
print(round(float(rb / ra - 1), 3))
print(round(float(2 * stats.norm.sf(abs(z))), 4))
