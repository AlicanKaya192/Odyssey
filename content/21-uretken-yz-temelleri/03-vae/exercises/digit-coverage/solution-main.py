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
    z = np.random.default_rng(seed).normal(size=(n, 2))
    images = decode(z, P)[1]
    counts = np.bincount(judge.predict(images), minlength=10)
    seen = int((counts >= 0.05 * n).sum())
    sure = judge.predict_proba(images).max(axis=1) > 0.9
    return [seen, round(float(sure.mean()), 3)]


print(coverage(1000, 1))
print(coverage(500, 2))
