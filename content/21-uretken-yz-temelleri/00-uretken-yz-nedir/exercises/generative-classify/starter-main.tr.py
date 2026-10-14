import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def log_density(point, mean, cov):
    diff = np.asarray(point, dtype=float) - mean
    inv = np.linalg.inv(cov)
    _, logdet = np.linalg.slogdet(cov)
    return -0.5 * (diff @ inv @ diff + logdet + 2 * np.log(2 * np.pi))


def classify(length, weight):
    return "perch"


for length, weight in [(22, 250), (33, 620), (27, 420), (29, 380)]:
    print(length, weight, classify(length, weight))
