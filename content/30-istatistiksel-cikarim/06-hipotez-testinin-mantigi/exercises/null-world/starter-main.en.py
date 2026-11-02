import numpy as np
from ab_data import make_population, make_speed_test

old = make_population()["load_ms"].to_numpy()
loads = make_speed_test(n=20, seed=81)
gap = abs(loads.mean() - old.mean())
rng = np.random.default_rng(82)
print(round(gap, 1))
# The H0 world: draw 10000 samples of 20 from old
# (rng.choice(old, size=(10000, 20))), take their means and print, with 3
# places, the share at least gap away from old.mean().
