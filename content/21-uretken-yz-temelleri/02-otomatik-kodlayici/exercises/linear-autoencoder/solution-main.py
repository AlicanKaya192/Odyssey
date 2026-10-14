import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def train_linear(k, steps, lr, seed):
    mean = X_train.mean(axis=0)
    A = X_train - mean
    rng = np.random.default_rng(seed)
    E = rng.normal(0, 0.1, (64, k))
    D = rng.normal(0, 0.1, (k, 64))
    for _ in range(steps):
        code = A @ E
        err = code @ D - A
        gD = code.T @ err * 2 / err.size
        gE = A.T @ (err @ D.T) * 2 / err.size
        E -= lr * gE
        D -= lr * gD
    rebuilt = (X_test - mean) @ E @ D + mean
    return round(float(((X_test - rebuilt) ** 2).mean()), 4)


print(train_linear(8, 500, 5.0, 0))
print(train_linear(8, 2000, 5.0, 0))
