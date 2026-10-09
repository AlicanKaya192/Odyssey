import numpy as np


def poly_train_mse(x, y, degree):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    A = np.column_stack([x ** d for d in range(degree + 1)])
    w = np.linalg.lstsq(A, y, rcond=None)[0]
    return round(float(((y - A @ w) ** 2).mean()), 4)

x = [-2, -1, 0, 1, 2, 3]
y = [4.1, 0.9, 0.1, 1.2, 3.9, 9.1]
for degree in (1, 2, 4):
    print(degree, poly_train_mse(x, y, degree))
