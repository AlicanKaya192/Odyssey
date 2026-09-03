import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("shoppers.csv")
columns = ["spend", "visits", "items", "returns"]
X = df[columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

counts = []
inertias = []
scores = []

for k in range(2, 9):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    inertia = float(model.inertia_)
    score = float(silhouette_score(X_scaled, labels))
    counts.append(k)
    inertias.append(inertia)
    scores.append(score)
    print(k, round(inertia, 1), round(score, 3))

figure, axes = plt.subplots(1, 2)
axes[0].plot(counts, inertias, marker="o")
axes[0].set_xlabel("k")
axes[0].set_ylabel("inertia")
axes[0].set_title("Elbow")
axes[1].plot(counts, scores, marker="o")
axes[1].set_xlabel("k")
axes[1].set_ylabel("silhouette")
axes[1].set_title("Silhouette")
figure.tight_layout()
figure.savefig("chart.png")

best = max(zip(counts, scores), key=lambda row: row[1])
print(best[0], round(best[1], 3))
