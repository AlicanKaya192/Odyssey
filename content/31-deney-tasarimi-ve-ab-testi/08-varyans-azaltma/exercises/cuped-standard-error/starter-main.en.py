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

# 1) Write se(y), the standard error of the difference (two groups, ddof=1).
# 2) Print the standard error of the plain minutes and of the CUPED minutes
#    (with pre), then the remaining variance ratio, with 3 places.
