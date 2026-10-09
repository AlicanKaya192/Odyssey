import numpy as np


def output_grads(H, p, y):
    H, p, y = (np.array(a, dtype=float) for a in (H, p, y))
    dz2 = (p - y)[:, None] / len(y)
    dW2 = H.T @ dz2
    return dW2.round(4).tolist(), round(float(dz2.sum()), 4)

H = [[0.5, -0.2], [0.1, 0.8], [-0.3, 0.4]]
dW2, db2 = output_grads(H, [0.7, 0.4, 0.9], [1, 0, 1])
print(dW2)
print(db2)
