from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=300, centers=3, random_state=4)
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def silhouette_table(ks):
    rows = []
    for k in ks:
        model = make_pipeline(StandardScaler(), KMeans(n_clusters=k, n_init=10, random_state=0))
        labels = model.fit_predict(X)
        rows.append([k, round(float(silhouette_score(X, labels)), 3)])
    return rows

print(*silhouette_table([2, 3, 4]), sep="\n")
