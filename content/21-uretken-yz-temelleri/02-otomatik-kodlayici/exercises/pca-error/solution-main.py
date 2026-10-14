import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def pca_error(k):
    mean = X_train.mean(axis=0)
    _, _, Vt = np.linalg.svd(X_train - mean, full_matrices=False)
    code = (X_test - mean) @ Vt[:k].T
    rebuilt = code @ Vt[:k] + mean
    return round(float(((X_test - rebuilt) ** 2).mean()), 4)


for k in [2, 8, 16]:
    print(k, pca_error(k))
