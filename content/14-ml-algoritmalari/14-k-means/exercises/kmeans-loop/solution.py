import numpy as np


def kmeans_loop(X, init, max_iter=100):
    X, C = np.array(X, dtype=float), np.array(init, dtype=float)
    rounds = 0
    for _ in range(max_iter):
        rounds += 1
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        new = np.array([X[labels == j].mean(axis=0) for j in range(len(C))])
        if np.allclose(new, C):
            break
        C = new
    return C.round(3).tolist(), rounds

X = [[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5], [3.5, 4.5]]
centers, rounds = kmeans_loop(X, [[1, 1], [5, 7]])
print(centers)
print(rounds)
