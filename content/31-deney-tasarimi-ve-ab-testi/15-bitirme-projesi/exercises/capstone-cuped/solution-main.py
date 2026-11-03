import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
y = test["revenue"].to_numpy()
x = test["pre_spend"].to_numpy()
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
adjusted = y - theta * (x - x.mean())
print(round(float(np.corrcoef(x, y)[0, 1]), 2))
print(round(float(adjusted.var() / y.var()), 3))
