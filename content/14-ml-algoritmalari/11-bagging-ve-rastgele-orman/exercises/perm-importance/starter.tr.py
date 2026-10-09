import numpy as np


def model_predict(X):
    return (X[:, 1] > 5).astype(int)


def perm_importance(X, y, seed):
    X, y = np.array(X, dtype=float), np.array(y)
    rng = np.random.default_rng(seed)
    base = (model_predict(X) == y).mean()
    # Her sutun icin karistir ve dusus.
    return []

rng = np.random.default_rng(4)
X = rng.uniform(0, 10, (300, 3))
y = (X[:, 1] > 5).astype(int)
print(perm_importance(X.tolist(), y.tolist(), 0))
