from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=80, seed=181)
means = test.groupby("layout")["minutes"].mean().round(2)
print(means.to_dict())
groups = [g["minutes"] for _, g in test.groupby("layout")]
result = stats.f_oneway(*groups)
print(round(result.statistic, 3), round(result.pvalue, 4))
