import numpy as np


def f(w):
    return (w[0] - 3) ** 2 + 2 * (w[1] + 1) ** 2 + w[0] * w[1]


def numeric_grad(w, eps=1e-6):
    w = np.array(w, dtype=float)
    grad = []
    for i in range(len(w)):
        step = np.zeros_like(w)
        step[i] = eps
        grad.append(round(float((f(w + step) - f(w - step)) / (2 * eps)), 4))
    return grad

print(numeric_grad([0.0, 0.0]))
print(numeric_grad([3.0, -1.0]))
