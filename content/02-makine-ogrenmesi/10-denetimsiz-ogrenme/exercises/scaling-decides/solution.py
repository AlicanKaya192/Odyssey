import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("shoppers.csv")
columns = ["spend", "visits", "items", "returns"]
X = df[columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

raw_labels = KMeans(n_clusters=4, random_state=42,
                    n_init=10).fit_predict(X)
scaled_labels = KMeans(n_clusters=4, random_state=42,
                       n_init=10).fit_predict(X_scaled)

for name, labels in (("raw", raw_labels), ("scaled", scaled_labels)):
    print(name, sorted(np.bincount(labels).tolist()),
          round(float(silhouette_score(X_scaled, labels)), 3))

df["cluster"] = raw_labels
print(df.groupby("cluster")[["spend", "visits"]].mean().round(1))

print(round(float(adjusted_rand_score(raw_labels, scaled_labels)), 3))
