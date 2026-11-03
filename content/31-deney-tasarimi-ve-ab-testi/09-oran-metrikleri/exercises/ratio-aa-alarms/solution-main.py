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


alarms = np.zeros(2)
for s in range(7000, 7400):
    t = make_pageviews(n=3000, seed=s)
    ra, va, ka, na = group_ratio(t[t["group"] == "A"])
    rb, vb, kb, nb = group_ratio(t[t["group"] == "B"])
    naive_se = np.sqrt(ra * (1 - ra) / na + rb * (1 - rb) / nb)
    delta_se = np.sqrt(va + vb)
    for j, se in enumerate([naive_se, delta_se]):
        alarms[j] += 2 * stats.norm.sf(abs(rb - ra) / se) < 0.05
print(alarms / 400)
