import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def sample_fish(name, n, seed):
    part = X[y == name]
    mean = part.mean(axis=0)
    cov = np.cov(part, rowvar=False)
    rng = np.random.default_rng(seed)
    return rng.multivariate_normal(mean, cov, size=n).round(1).tolist()


for fish in sample_fish("bream", 3, 1):
    print(fish)
