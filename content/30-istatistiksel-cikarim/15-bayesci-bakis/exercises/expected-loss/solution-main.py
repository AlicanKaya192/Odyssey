import numpy as np
from ab_data import make_checkout_test

shop = make_checkout_test(n=1500, seed=513)
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
rng = np.random.default_rng(514)
draw_a = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 100_000)
draw_b = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 100_000)
loss_b = np.maximum(draw_a - draw_b, 0).mean()
loss_a = np.maximum(draw_b - draw_a, 0).mean()
print(f"{loss_b:.5f}", f"{loss_a:.5f}")
print("B" if loss_b < 0.001 else "wait")
