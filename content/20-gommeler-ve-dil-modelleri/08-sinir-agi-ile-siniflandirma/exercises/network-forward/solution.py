import numpy as np


def forward(A, E, W1, W2):
    x = np.array(A) @ np.array(E)
    h = np.maximum(x @ np.array(W1), 0)
    z = h @ np.array(W2)
    z = z - z.max(axis=1, keepdims=True)
    p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
    return p.round(3).tolist()

E = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
W1 = [[1.0, -1.0], [0.5, 1.0]]
W2 = [[1.0, 0.0], [0.0, 1.0]]
print(forward([[0.0, 0.5, 0.5]], E, W1, W2))
print(forward([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], E, W1, W2))
