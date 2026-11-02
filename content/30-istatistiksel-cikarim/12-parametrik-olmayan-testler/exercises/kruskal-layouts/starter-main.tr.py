from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=60, seed=213)
groups = [g["minutes"] for _, g in test.groupby("layout")]
# Önce Kruskal-Wallis'in p'sini (stats.kruskal), sonra ANOVA'nın p'sini
# (stats.f_oneway) 4 basamakla alt alta yazdır.
