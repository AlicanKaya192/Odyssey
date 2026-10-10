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
import json

import numpy as np

scaler, clf = model[0], model[-1]
TEXT = json.dumps({"mean": scaler.mean_.tolist(), "scale": scaler.scale_.tolist(),
                   "coef": clf.coef_[0].tolist(), "intercept": float(clf.intercept_[0])})


def json_proba(rows):
    p = json.loads(TEXT)
    z = (np.array(rows) - np.array(p["mean"])) / np.array(p["scale"])
    proba = 1 / (1 + np.exp(-(z @ np.array(p["coef"]) + p["intercept"])))
    return proba.round(3).tolist()

print(json_proba([[0.5, -1.0, 0.3, 1.2], [-0.2, 1.5, -0.7, 0.0]]))
