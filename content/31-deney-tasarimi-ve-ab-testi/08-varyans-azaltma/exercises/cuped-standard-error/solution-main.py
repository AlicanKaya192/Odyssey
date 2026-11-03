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


def se(y):
    return np.sqrt(y[is_b].var(ddof=1) / is_b.sum() + y[~is_b].var(ddof=1) / (~is_b).sum())


adjusted = cuped(minutes, pre)
print(round(float(se(minutes)), 3))
print(round(float(se(adjusted)), 3))
print(round(float(adjusted.var() / minutes.var()), 3))
