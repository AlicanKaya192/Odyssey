import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def denoise(k, sigma, seed):
    noisy = X_test + np.random.default_rng(seed).normal(0, sigma, X_test.shape)
    mean = X_train.mean(axis=0)
    _, _, Vt = np.linalg.svd(X_train - mean, full_matrices=False)
    rebuilt = ((noisy - mean) @ Vt[:k].T) @ Vt[:k] + mean
    before = ((noisy - X_test) ** 2).mean()
    after = ((rebuilt - X_test) ** 2).mean()
    return [round(float(before), 4), round(float(after), 4)]


for k in [8, 16, 32]:
    print(k, denoise(k, 0.2, 3))
