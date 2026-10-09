import numpy as np


def centroid_fit(X, y):
    return {c: X[y == c].mean(axis=0) for c in np.unique(y)}


def centroid_predict(centers, X):
    labels = list(centers)
    dists = np.stack([((X - centers[c]) ** 2).sum(axis=1) for c in labels])
    return np.array(labels)[dists.argmin(axis=0)]


def cv_accuracy(X, y, k):
    X, y = np.array(X), np.array(y)
    n = len(y)
    scores = []
    # Her kat: test araligi, egitim = geri kalan.
    return round(float(np.mean(scores)), 3) if scores else 0.0

rng = np.random.default_rng(2)
y = (rng.random(60) < 0.4).astype(int)
X = rng.normal(0, 1, size=(60, 2)) + y[:, None] * 1.5
print(cv_accuracy(X.tolist(), y.tolist(), 5))
