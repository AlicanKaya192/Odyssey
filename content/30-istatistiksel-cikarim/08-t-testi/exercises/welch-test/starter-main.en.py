from scipy import stats
from ab_data import make_design_test

test = make_design_test(n=200, seed=121)
a = test.loc[test["group"] == "A", "minutes"]
b = test.loc[test["group"] == "B", "minutes"]
result = stats.ttest_ind(a, b, equal_var=False)
low, high = result.confidence_interval(0.95)
print(round(b.mean() - a.mean(), 2))
print(round(result.pvalue, 4))
print(round(low, 2), round(high, 2))
