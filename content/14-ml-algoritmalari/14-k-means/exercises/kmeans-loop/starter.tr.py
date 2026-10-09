import numpy as np


def kmeans_loop(X, init, max_iter=100):
    X, C = np.array(X, dtype=float), np.array(init, dtype=float)
    rounds = 0
    # Ata, guncelle, durdu mu?
    return C.round(3).tolist(), rounds

X = [[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5], [3.5, 4.5]]
centers, rounds = kmeans_loop(X, [[1, 1], [5, 7]])
print(centers)
print(rounds)
