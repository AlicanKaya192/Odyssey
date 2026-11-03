import numpy as np
from ab_data import make_engagement_test


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())

# make_engagement_test(n=8000, seed=s) ile s = 300..349 arası 50 deney kur.
# Her deneyde B - A dakika farkını üç biçimde hesapla:
# 1) düz, 2) pre_minutes ile CUPED, 3) sessions (test sırası) ile CUPED.
# Üç farkın 50 deneydeki ortalamasını alt alta 3 basamakla yaz.
