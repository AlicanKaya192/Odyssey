import numpy as np

rng = np.random.default_rng(5)
centers = rng.normal(size=(30, 4))
labels = rng.integers(0, 2, size=30)
groups = np.repeat(np.arange(30), 5)
X = centers[groups] + rng.normal(scale=0.1, size=(150, 4))
y = labels[groups]
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


def honest_score(k):
    model = KNeighborsClassifier(n_neighbors=k)
    plain = cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0))
    grouped = cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0))
    return [round(float(plain.mean()), 3), round(float(grouped.mean()), 3)]

print(honest_score(3))
