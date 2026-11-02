import itertools
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
names = sorted(test["layout"].unique())
groups = [test.loc[test["layout"] == n, "minutes"] for n in names]
for i, j in itertools.combinations(range(4), 2):
    if stats.ttest_ind(groups[i], groups[j]).pvalue < 0.05:
        print(names[i], names[j])
