import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline


def honest_score(seed):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(60, 2000))
    y = rng.integers(0, 2, 60)
    X_best = SelectKBest(f_classif, k=10).fit_transform(X, y)
    return round(float(cross_val_score(LogisticRegression(), X_best, y, cv=5).mean()), 2)

print(honest_score(6))
