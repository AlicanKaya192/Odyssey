import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("shoppers.csv")
columns = ["spend", "visits", "items", "returns"]
X = df[columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score

full_pca = PCA()
full_pca.fit(X_scaled)
cumulative = np.cumsum(full_pca.explained_variance_ratio_)
print([round(float(value), 3) for value in cumulative])

pca = PCA(n_components=2)
Z = pca.fit_transform(X_scaled)
for component in pca.components_:
    print([round(float(weight), 3) for weight in component])

full_labels = KMeans(n_clusters=4, random_state=42,
                     n_init=10).fit_predict(X_scaled)
pca_labels = KMeans(n_clusters=4, random_state=42, n_init=10).fit_predict(Z)

print(round(float(silhouette_score(X_scaled, full_labels)), 3),
      round(float(silhouette_score(Z, pca_labels)), 3))
print(round(float(adjusted_rand_score(full_labels, pca_labels)), 3))

plt.scatter(Z[:, 0], Z[:, 1], c=full_labels)
plt.xlabel("pc1")
plt.ylabel("pc2")
plt.title("Shoppers in two components")
plt.savefig("chart.png")
