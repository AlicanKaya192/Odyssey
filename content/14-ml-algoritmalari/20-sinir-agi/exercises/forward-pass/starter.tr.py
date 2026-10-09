import numpy as np


def forward_pass(X, W1, b1, W2, b2):
    X, W1, W2 = (np.array(a, dtype=float) for a in (X, W1, W2))
    b1, b2 = np.array(b1, dtype=float), np.array(b2, dtype=float)
    # tanh, sonra sigmoid
    return []

X = [[0.0, 0.0], [1.0, 1.0], [1.0, -1.0]]
W1 = [[1.0, -1.0], [0.5, 2.0]]
W2 = [[1.5], [-1.0]]
print(forward_pass(X, W1, [0.0, 0.1], W2, [0.2]))
