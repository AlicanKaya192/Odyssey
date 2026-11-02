import numpy as np


def unpicked_share(n, seed=0):
    rng = np.random.default_rng(seed)
    picked = rng.choice(n, n)
    return round(1 - len(np.unique(picked)) / n, 3)


print(unpicked_share(1000))
print(unpicked_share(100000))
