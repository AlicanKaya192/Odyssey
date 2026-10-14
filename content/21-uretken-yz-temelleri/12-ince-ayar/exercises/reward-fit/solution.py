import numpy as np


def fit_reward(diffs, steps, lr):
    D = np.array(diffs, dtype=float)
    w = np.zeros(D.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-D @ w))
        w += lr * D.T @ (1 - p) / len(D)
    return [round(float(v), 2) for v in w]


print(fit_reward([[1, 0], [1, 1], [0, 1], [1, -1]], 2000, 0.5))
