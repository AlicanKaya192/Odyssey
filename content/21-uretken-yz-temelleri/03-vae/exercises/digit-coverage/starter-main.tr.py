import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X_train, X_test = X[order[:1500]], X[order[1500:]]
from sklearn.linear_model import LogisticRegression
from vae_model import train_vae, decode

judge = LogisticRegression(max_iter=2000).fit(X_train, y[order[:1500]])
P = train_vae(X_train, 2, beta=1.0)


def coverage(n, seed):
    return [0, 0.0]


print(coverage(1000, 1))
print(coverage(500, 2))
