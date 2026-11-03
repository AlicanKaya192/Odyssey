import numpy as np
from ab_data import make_engagement_test


def cuped(y, x):
    theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
    return y - theta * (x - x.mean())


diffs = []
for s in range(300, 350):
    t = make_engagement_test(n=8000, seed=s)
    b = (t["group"] == "B").to_numpy()
    y = t["minutes"].to_numpy()
    row = []
    for adjusted in [y, cuped(y, t["pre_minutes"].to_numpy()),
                     cuped(y, t["sessions"].to_numpy())]:
        row.append(adjusted[b].mean() - adjusted[~b].mean())
    diffs.append(row)
for value in np.mean(diffs, axis=0):
    print(round(float(value), 3))
