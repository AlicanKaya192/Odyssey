import numpy as np


def assign_cities(user_cities, seed=0):
    rng = np.random.default_rng(seed)
    in_b = rng.random(len(user_cities)) < 0.5
    return sorted({c for c, b in zip(user_cities, in_b) if b})


print(assign_cities(["X", "X", "Y", "Z", "Y", "W"]))
