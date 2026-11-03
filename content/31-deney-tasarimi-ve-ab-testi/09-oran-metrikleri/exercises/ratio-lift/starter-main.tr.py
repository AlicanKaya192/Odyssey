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
# 1) İki grubun oranını (4 basamak) aynı satırda yaz: önce A, sonra B.
# 2) Göreli artışı (rb / ra - 1) 3 basamakla yaz.
# 3) Delta yöntemiyle iki yönlü p'yi 4 basamakla yaz.
