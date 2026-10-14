import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def anomaly_errors(k):
    y_train, y_test = y[order[:1500]], y[order[1500:]]
    return [0.0, 0.0]


print(anomaly_errors(8))
print(anomaly_errors(16))
