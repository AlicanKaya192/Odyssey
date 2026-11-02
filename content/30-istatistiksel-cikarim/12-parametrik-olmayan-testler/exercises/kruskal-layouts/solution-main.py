from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=60, seed=213)
groups = [g["minutes"] for _, g in test.groupby("layout")]
print(round(stats.kruskal(*groups).pvalue, 4))
print(round(stats.f_oneway(*groups).pvalue, 4))
