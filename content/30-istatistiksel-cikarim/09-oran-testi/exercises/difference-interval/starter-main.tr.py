from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_checkout_test

test = make_checkout_test(n=3000, seed=141)
groups = test.groupby("group")["bought"]
k, n = groups.sum(), groups.count()
low, high = confint_proportions_2indep(k["A"], n["A"], k["B"], n["B"],
                                       method="newcomb")
print(round(low, 4), round(high, 4))
