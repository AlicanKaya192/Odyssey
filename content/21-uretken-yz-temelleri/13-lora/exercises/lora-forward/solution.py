import numpy as np


def lora_forward(x, W, A, B):
    x, W, A, B = (np.array(m, dtype=float) for m in (x, W, A, B))
    return (x @ W + (x @ A) @ B).round(3).tolist()


x = [[1.0, 2.0]]
W = [[1.0, 0.0], [0.0, 1.0]]
A = [[0.5], [0.0]]
B = [[0.0, 2.0]]
print(lora_forward(x, W, A, B))
