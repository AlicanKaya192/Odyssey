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

model = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)

print(np.bincount(labels).tolist())

df["cluster"] = labels
print(df.groupby("cluster")[columns].mean().round(1))

print(round(float(silhouette_score(X_scaled, labels)), 3))
