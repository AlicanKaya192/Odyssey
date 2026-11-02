import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=2000, seed=613)
k = shop.groupby("group")["bought"].sum()
rng = np.random.default_rng(614)
draw_a = rng.beta(1 + k["A"], 1 + 2000 - k["A"], 100_000)
draw_b = rng.beta(1 + k["B"], 1 + 2000 - k["B"], 100_000)
p = proportions_ztest([k["B"], k["A"]], [2000, 2000],
                      alternative="larger")[1]
print(round(p, 4), round(1 - (draw_b > draw_a).mean(), 4))
