from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def pca_components(ratio):
    scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=10).fit(scaled)
    kept = pca.explained_variance_ratio_.sum()
    return [int(pca.n_components_), round(float(kept), 3)]

print(pca_components(0.95))
print(pca_components(0.5))
