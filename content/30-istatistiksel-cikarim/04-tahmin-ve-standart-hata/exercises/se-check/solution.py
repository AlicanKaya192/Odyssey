import numpy as np


def se_check(values, n, reps, seed):
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(reps, n))
    real = samples.mean(axis=1).std()
    estimated = (samples.std(axis=1, ddof=1) / np.sqrt(n)).mean()
    return [round(float(real), 3), round(float(estimated), 3)]


data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 9, 15, 30]
print(se_check(data, 5, 4000, 0))
print(se_check(data, 40, 4000, 0))
