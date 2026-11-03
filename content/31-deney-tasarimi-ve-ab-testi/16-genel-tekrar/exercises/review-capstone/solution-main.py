import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=84, lift=0.06)
n = test.groupby("group").size()
k = test.groupby("group")["bought"].sum()
print(round(float(stats.chisquare(n).pvalue), 3))
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print(round(low * 100, 2), round(high * 100, 2))
y = test["revenue"].to_numpy()
x = test["pre_spend"].to_numpy()
print(round(float(1 - np.corrcoef(x, y)[0, 1] ** 2), 3))
