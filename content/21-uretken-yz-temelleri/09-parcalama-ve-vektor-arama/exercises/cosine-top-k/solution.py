import numpy as np


def top_k(vectors, query, k):
    V = np.array(vectors, dtype=float)
    q = np.array(query, dtype=float)
    scores = V @ q / (np.linalg.norm(V, axis=1) * np.linalg.norm(q))
    order = sorted(range(len(scores)), key=lambda i: (-round(float(scores[i]), 9), i))
    return order[:k]


print(top_k([[1, 0], [0.6, 0.8], [0, 1]], [1, 1], 2))
print(top_k([[3, 0], [0, 2]], [0, 5], 1))
