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

# group_ratio gives a group's ratio, delta variance, total clicks and
# total views.
# Build 400 A/A experiments with make_pageviews(n=3000, seed=s), s = 7000..7399.
# In each, compute the two-sided p with two standard errors:
#   naive: sqrt(ra * (1 - ra) / na + rb * (1 - rb) / nb)
#   delta: sqrt(va + vb)
# Print the share with p < 0.05 as an array [naive delta].
