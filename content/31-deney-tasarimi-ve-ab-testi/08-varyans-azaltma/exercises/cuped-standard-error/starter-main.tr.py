import numpy as np
from ab_data import make_engagement_test

test = make_engagement_test(n=8000, seed=21)
is_b = (test["group"] == "B").to_numpy()
minutes = test["minutes"].to_numpy()
pre = test["pre_minutes"].to_numpy()
sessions = test["sessions"].to_numpy()


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())

# 1) Farkın standart hatasını veren se(y) fonksiyonunu yaz (iki grup, ddof=1).
# 2) Düz dakikaların ve CUPED'li dakikaların (pre ile) standart hatasını,
#    sonra kalan varyans oranını 3 basamakla yaz.
