import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]


def kept_share(k):
    return 0.0


for k in [2, 8, 16, 32]:
    print(k, kept_share(k))
