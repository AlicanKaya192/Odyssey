import numpy as np


def self_attention(X):
    X = np.array(X)
    scores = X @ X.T / np.sqrt(X.shape[1])
    scores = scores - scores.max(axis=1, keepdims=True)
    weights = np.exp(scores)
    weights = weights / weights.sum(axis=1, keepdims=True)
    return weights.round(3).tolist()

X = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
for row in self_attention(X):
    print(row)
