import numpy as np


def efficiency_ratio(values, n, reps, seed):
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(reps, n))
    sd_mean = samples.mean(axis=1).std()
    sd_median = np.median(samples, axis=1).std()
    return round(float((sd_median / sd_mean) ** 2), 2)


flat = list(range(1, 101))
print(efficiency_ratio(flat, 25, 3000, 0))
