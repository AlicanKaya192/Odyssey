import numpy as np
from ab_data import make_population, make_speed_test

old = make_population()["load_ms"].to_numpy()
loads = make_speed_test(n=20, seed=81)
gap = abs(loads.mean() - old.mean())
rng = np.random.default_rng(82)
means = rng.choice(old, size=(10000, 20)).mean(axis=1)
far = np.abs(means - old.mean()) >= gap
print(round(gap, 1))
print(round(far.mean(), 3))
