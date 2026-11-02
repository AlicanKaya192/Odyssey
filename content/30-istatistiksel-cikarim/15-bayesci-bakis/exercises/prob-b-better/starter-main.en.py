import numpy as np
from ab_data import make_checkout_test

shop = make_checkout_test(n=1500, seed=511)
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
rng = np.random.default_rng(512)
# 1) Draw 100_000 samples from each posterior with a flat prior (A first).
# 2) Print P(B > A) with 3 places.
# 3) Print the 95% credible interval of the difference (B - A), 4 places.
