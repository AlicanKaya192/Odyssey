import numpy as np
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
X = data.data.iloc[:, :5].copy()
y = data.target
rng = np.random.default_rng(0)
X["row_id"] = rng.permutation(len(X))
X["coin"] = rng.integers(0, 2, len(X))
from sklearn.ensemble import RandomForestClassifier


def top_columns(k):
    rf = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
    return list(X.columns[:k])

print(top_columns(2))
print(top_columns(7)[-2:])
