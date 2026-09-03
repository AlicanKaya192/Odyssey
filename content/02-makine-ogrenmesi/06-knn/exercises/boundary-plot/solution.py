import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("customers.csv")
X = df[["income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

grid_x, grid_y = np.meshgrid(np.linspace(-2.5, 2.5, 200),
                             np.linspace(-2.5, 2.5, 200))
grid = np.c_[grid_x.ravel(), grid_y.ravel()]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

for ax, k in zip(axes, (1, 15)):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    zone = model.predict(grid).reshape(grid_x.shape)
    ax.contourf(grid_x, grid_y, zone, alpha=0.25, levels=1)
    ax.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], c=y_train, s=14)
    score = accuracy_score(y_test, model.predict(X_test_scaled))
    ax.set_title(f"k = {k}")
    ax.set_xlabel("income (scaled)")
    ax.set_ylabel("visits (scaled)")
    print(k, round(score, 3))

fig.tight_layout()
fig.savefig("chart.png")
