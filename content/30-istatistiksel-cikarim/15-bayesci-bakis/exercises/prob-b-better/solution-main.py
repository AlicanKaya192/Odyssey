import numpy as np
from ab_data import make_checkout_test

shop = make_checkout_test(n=1500, seed=511)
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
rng = np.random.default_rng(512)
draw_a = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 100_000)
draw_b = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 100_000)
print(round((draw_b > draw_a).mean(), 3))
low, high = np.percentile(draw_b - draw_a, [2.5, 97.5])
print(round(low, 4), round(high, 4))
