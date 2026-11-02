import itertools
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
names = sorted(test["layout"].unique())
groups = [test.loc[test["layout"] == n, "minutes"] for n in names]
res = stats.tukey_hsd(*groups)
for i, j in itertools.combinations(range(4), 2):
    if res.pvalue[i, j] < 0.05:
        print(names[i], names[j])
