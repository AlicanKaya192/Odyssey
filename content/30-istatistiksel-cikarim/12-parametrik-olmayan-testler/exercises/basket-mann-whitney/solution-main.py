import numpy as np
from scipy import stats
from ab_data import make_basket_test

test = make_basket_test(n=150, seed=211)
a = test.loc[test["group"] == "A", "basket"].to_numpy()
b = test.loc[test["group"] == "B", "basket"].to_numpy()
u = stats.mannwhitneyu(b, a)
print(round(np.median(a), 1), round(np.median(b), 1))
print(round(u.pvalue, 4))
print(round(u.statistic / (len(a) * len(b)), 3))
