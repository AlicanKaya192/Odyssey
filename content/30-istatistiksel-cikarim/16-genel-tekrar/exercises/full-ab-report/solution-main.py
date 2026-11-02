from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=6000, seed=611)
k = shop.groupby("group")["bought"].sum()
print(round(k["A"] / 6000, 4), round(k["B"] / 6000, 4))
p = proportions_ztest([k["B"], k["A"]], [6000, 6000])[1]
print(round(p, 4))
low, high = confint_proportions_2indep(k["B"], 6000, k["A"], 6000)
print(round(low, 4), round(high, 4))
