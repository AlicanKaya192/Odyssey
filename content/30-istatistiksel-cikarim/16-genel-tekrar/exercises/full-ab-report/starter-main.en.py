from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=6000, seed=611)
k = shop.groupby("group")["bought"].sum()
# Print, one per line:
# 1) the buying rates of A and B (4 places)
# 2) the p of the two-sided z-test (4 places)
# 3) the 95% confidence interval of the difference (B - A) (4 places)
