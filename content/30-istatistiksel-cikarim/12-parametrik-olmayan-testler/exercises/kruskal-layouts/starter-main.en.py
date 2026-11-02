from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=60, seed=213)
groups = [g["minutes"] for _, g in test.groupby("layout")]
# Print the p of Kruskal-Wallis (stats.kruskal) first, then the p of ANOVA
# (stats.f_oneway), with 4 places, one per line.
