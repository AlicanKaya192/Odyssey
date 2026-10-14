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
    best, best_score = None, None
    for name in ["perch", "bream"]:
        part = X[y == name]
        mean = part.mean(axis=0)
        cov = np.cov(part, rowvar=False)
        score = log_density([length, weight], mean, cov) + np.log(np.mean(y == name))
        if best_score is None or score > best_score:
            best, best_score = name, score
    return best


for length, weight in [(22, 250), (33, 620), (27, 420), (29, 380)]:
    print(length, weight, classify(length, weight))
