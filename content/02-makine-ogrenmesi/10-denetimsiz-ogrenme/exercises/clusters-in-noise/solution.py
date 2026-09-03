import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("shoppers.csv")
columns = ["spend", "visits", "items", "returns"]
X = df[columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

rng = np.random.default_rng(0)
noise = rng.normal(0, 1, X_scaled.shape)

real_four = 0.0
noise_four = 0.0
noise_sizes = []

for k in range(2, 6):
    real_labels = KMeans(n_clusters=k, random_state=42,
                         n_init=10).fit_predict(X_scaled)
    noise_labels = KMeans(n_clusters=k, random_state=42,
                          n_init=10).fit_predict(noise)
    real_score = float(silhouette_score(X_scaled, real_labels))
    noise_score = float(silhouette_score(noise, noise_labels))
    if k == 4:
        real_four = real_score
        noise_four = noise_score
        noise_sizes = sorted(np.bincount(noise_labels).tolist())
    print(k, round(real_score, 3), round(noise_score, 3))

print(noise_sizes)
print(round(real_four / noise_four, 1))
