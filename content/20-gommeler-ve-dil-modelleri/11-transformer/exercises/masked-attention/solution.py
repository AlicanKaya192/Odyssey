import numpy as np


def masked_attention(X):
    X = np.array(X)
    n, d = X.shape
    scores = X @ X.T / np.sqrt(d)
    scores = np.where(np.tril(np.ones((n, n), dtype=bool)), scores, -np.inf)
    weights = np.exp(scores - scores.max(axis=1, keepdims=True))
    weights = weights / weights.sum(axis=1, keepdims=True)
    return weights.round(3).tolist()

for row in masked_attention([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]):
    print(row)
