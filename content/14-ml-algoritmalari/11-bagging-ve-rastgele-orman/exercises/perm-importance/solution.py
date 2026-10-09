import numpy as np


def model_predict(X):
    return (X[:, 1] > 5).astype(int)


def perm_importance(X, y, seed):
    X, y = np.array(X, dtype=float), np.array(y)
    rng = np.random.default_rng(seed)
    base = (model_predict(X) == y).mean()
    drops = []
    for j in range(X.shape[1]):
        Xp = X.copy()
        Xp[:, j] = rng.permutation(Xp[:, j])
        drops.append(round(float(base - (model_predict(Xp) == y).mean()), 3))
    return drops

rng = np.random.default_rng(4)
X = rng.uniform(0, 10, (300, 3))
y = (X[:, 1] > 5).astype(int)
print(perm_importance(X.tolist(), y.tolist(), 0))
