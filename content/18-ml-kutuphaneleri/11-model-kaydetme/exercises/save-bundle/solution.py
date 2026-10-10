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
import joblib
import sklearn


def save_bundle(path, threshold):
    bundle = {"model": model, "sklearn": sklearn.__version__, "columns": COLUMNS,
              "threshold": threshold}
    joblib.dump(bundle, path)
    loaded = joblib.load(path)
    return [sorted(loaded), loaded["threshold"], loaded.get("columns")]

print(*save_bundle("churn.joblib", 0.3), sep="\n")
