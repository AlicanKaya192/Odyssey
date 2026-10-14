import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def train_linear(k, steps, lr, seed):
    mean = X_train.mean(axis=0)
    A = X_train - mean
    return 0.0


print(train_linear(8, 500, 5.0, 0))
print(train_linear(8, 2000, 5.0, 0))
