import numpy as np
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_capstone

test = make_capstone(seed=83, lift=0.0)
n = test.groupby("group").size()
print(round(float(stats.chisquare(n).pvalue), 3))
k = test.groupby("group")["bought"].sum()
low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
print(round(low * 100, 2), round(high * 100, 2))
