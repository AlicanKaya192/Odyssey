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
import pickle
import warnings

import sklearn
from sklearn.exceptions import InconsistentVersionWarning


def stop_old_version(version):
    data = pickle.dumps(LogisticRegression().fit(X, y))
    old_file = data.replace(sklearn.__version__.encode(), version.encode())
    with warnings.catch_warnings():
        warnings.simplefilter("error", InconsistentVersionWarning)
        try:
            pickle.loads(old_file)
        except InconsistentVersionWarning as warning:
            return [warning.estimator_name, warning.original_sklearn_version]
    return ["loaded", version]

print(stop_old_version("1.2.2"))
