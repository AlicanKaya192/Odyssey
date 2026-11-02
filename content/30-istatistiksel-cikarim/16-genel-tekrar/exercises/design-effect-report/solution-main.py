import numpy as np
from scipy import stats
from ab_data import make_design_test

test = make_design_test(n=200, seed=612)
a = test.loc[test["group"] == "A", "minutes"].to_numpy()
b = test.loc[test["group"] == "B", "minutes"].to_numpy()
print(round(np.median(a), 2), round(np.median(b), 2))
print(round(stats.ttest_ind(b, a, equal_var=False).pvalue, 4))
print(round(stats.mannwhitneyu(b, a).pvalue, 4))
pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
print(round((b.mean() - a.mean()) / pooled, 3))
