from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=6000, seed=611)
k = shop.groupby("group")["bought"].sum()
# Alt alta yaz:
# 1) A ve B'nin satın alma oranları (4 basamak)
# 2) iki yönlü z-testinin p'si (4 basamak)
# 3) farkın (B - A) %95 güven aralığı (4 basamak)
