import numpy as np


def sample_stats(mu, logvar, n, seed):
    rng = np.random.default_rng(seed)
    mu = np.array(mu)
    std = np.exp(0.5 * np.array(logvar))
    z = mu + std * rng.normal(size=(n, len(mu)))
    means = [round(float(a), 2) for a in z.mean(axis=0)]
    stds = [round(float(a), 2) for a in z.std(axis=0)]
    return means + stds


print(sample_stats([1.5, -0.5], [-2.0, 0.0], 10000, 0))
print(sample_stats([0.0], [1.0], 5000, 3))
