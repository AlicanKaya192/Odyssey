from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def nan_forest(rate):
    X_nan = X_train.copy()
    rng = np.random.default_rng(0)
    X_nan[rng.random(X_nan.shape) < rate] = np.nan
    model = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_nan, y_train)
    return round(float(model.score(X_test, y_test)), 3)

print(nan_forest(0.1))
print(nan_forest(0.3))
