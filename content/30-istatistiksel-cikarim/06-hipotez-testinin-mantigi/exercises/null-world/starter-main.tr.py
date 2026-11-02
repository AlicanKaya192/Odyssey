import numpy as np
from ab_data import make_population, make_speed_test

old = make_population()["load_ms"].to_numpy()
loads = make_speed_test(n=20, seed=81)
gap = abs(loads.mean() - old.mean())
rng = np.random.default_rng(82)
print(round(gap, 1))
# H0 dünyası: old'dan 10000 tane 20'lik örneklem çek
# (rng.choice(old, size=(10000, 20))), ortalamalarını al ve
# old.mean()'den en az gap kadar uzak olanların payını 3 basamakla yazdır.
