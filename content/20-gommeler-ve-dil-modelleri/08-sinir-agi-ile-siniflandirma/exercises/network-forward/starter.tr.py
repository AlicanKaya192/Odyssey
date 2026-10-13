import numpy as np


def forward(A, E, W1, W2):
    return []

E = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
W1 = [[1.0, -1.0], [0.5, 1.0]]
W2 = [[1.0, 0.0], [0.0, 1.0]]
print(forward([[0.0, 0.5, 0.5]], E, W1, W2))
print(forward([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], E, W1, W2))
