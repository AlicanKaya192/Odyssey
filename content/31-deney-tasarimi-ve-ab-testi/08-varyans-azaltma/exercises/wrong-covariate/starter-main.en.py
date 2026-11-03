import numpy as np
from ab_data import make_engagement_test


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())

# Build 50 experiments with make_engagement_test(n=8000, seed=s) for
# s = 300..349. In each, compute the B - A minutes difference three ways:
# 1) plain, 2) CUPED with pre_minutes, 3) CUPED with sessions (during).
# Print the averages of the three differences over the 50 experiments,
# one per line, with 3 places.
