from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=300, centers=3, random_state=4)
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, adjusted_rand_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def cluster_ari(k):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0)
    labels = make_pipeline(StandardScaler(), kmeans).fit_predict(X)
    return round(float(adjusted_rand_score(y, labels)), 3)

print(cluster_ari(3))
print(cluster_ari(2))
