import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def anomaly_errors(k):
    y_train, y_test = y[order[:1500]], y[order[1500:]]
    seen = X_train[y_train < 5]
    mean = seen.mean(axis=0)
    _, _, Vt = np.linalg.svd(seen - mean, full_matrices=False)
    rebuilt = ((X_test - mean) @ Vt[:k].T) @ Vt[:k] + mean
    errors = ((X_test - rebuilt) ** 2).mean(axis=1)
    return [round(float(errors[y_test < 5].mean()), 4), round(float(errors[y_test >= 5].mean()), 4)]


print(anomaly_errors(8))
print(anomaly_errors(16))
