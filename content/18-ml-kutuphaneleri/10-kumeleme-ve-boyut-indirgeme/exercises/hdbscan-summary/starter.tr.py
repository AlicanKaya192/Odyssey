import numpy as np
from sklearn.datasets import make_blobs, make_moons

moons, y_moons = make_moons(n_samples=400, noise=0.06, random_state=0)
blob, _ = make_blobs(n_samples=150, centers=[[2.5, 1.8]], cluster_std=0.12,
                     random_state=1)
X = np.vstack([moons, blob])
y = np.concatenate([y_moons, np.full(150, 2)])
from sklearn.cluster import DBSCAN, HDBSCAN
from sklearn.metrics import adjusted_rand_score


def hdbscan_summary(size):
    labels = DBSCAN(eps=0.1, min_samples=10).fit_predict(X)
    clusters = len(set(labels) - {-1})
    noise = int((labels == -1).sum())
    return [clusters, noise, round(float(adjusted_rand_score(y, labels)), 3)]

print(hdbscan_summary(20))
print(hdbscan_summary(5))
