import numpy as np


def expected_loss(k_a, n_a, k_b, n_b, draws=100000, seed=0):
    rng = np.random.default_rng(seed)
    pa = rng.beta(1 + k_a, 1 + n_a - k_a, draws)
    pb = rng.beta(1 + k_b, 1 + n_b - k_b, draws)
    return round(float((pa - pb).mean()), 5)


print(expected_loss(240, 2000, 270, 2000))
