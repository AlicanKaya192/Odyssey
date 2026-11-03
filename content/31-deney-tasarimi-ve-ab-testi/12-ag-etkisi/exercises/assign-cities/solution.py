import numpy as np


def assign_cities(user_cities, seed=0):
    rng = np.random.default_rng(seed)
    cities = sorted(set(user_cities))
    order = rng.permutation(len(cities))
    return sorted(cities[i] for i in order[: len(cities) // 2])


print(assign_cities(["X", "X", "Y", "Z", "Y", "W"]))
