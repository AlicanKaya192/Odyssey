import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=4, n_informative=3,
                           n_redundant=0, random_state=2)
COLUMNS = ["age", "income", "visits", "score"]
X = pd.DataFrame(X, columns=COLUMNS)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
import os

import joblib
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)


def forest_size(level):
    joblib.dump(forest, "forest.joblib")
    return os.path.getsize("forest.joblib") // 1024

print(forest_size(0))
print(forest_size(3))
