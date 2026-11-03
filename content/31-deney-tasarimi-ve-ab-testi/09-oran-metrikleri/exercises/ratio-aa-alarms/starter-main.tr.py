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

# group_ratio bir grubun oranını, delta varyansını, toplam tıklamayı ve
# toplam gösterimi veriyor.
# make_pageviews(n=3000, seed=s) ile s = 7000..7399 arası 400 A/A deneyi kur.
# Her deneyde iki standart hatayla iki yönlü p hesapla:
#   saf: sqrt(ra * (1 - ra) / na + rb * (1 - rb) / nb)
#   delta: sqrt(va + vb)
# p < 0.05 olanların payını [saf delta] dizisi olarak yaz.
