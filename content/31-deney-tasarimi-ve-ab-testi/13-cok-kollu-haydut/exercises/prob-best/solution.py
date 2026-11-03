import numpy as np


def prob_best(k, n, draws=20000, seed=0):
    rng = np.random.default_rng(seed)
    k, n = np.asarray(k), np.asarray(n)
    samples = rng.beta(1 + k, 1 + n - k, (draws, len(k)))
    best = samples.argmax(axis=1)
    return [round(float((best == j).mean()), 3) for j in range(len(k))]


print(prob_best([12, 30, 25], [300, 500, 400]))
