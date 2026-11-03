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
# 1) Print the two groups' ratios (4 places) on one line: A first, then B.
# 2) Print the relative lift (rb / ra - 1) with 3 places.
# 3) Print the two-sided p by the delta method with 4 places.
