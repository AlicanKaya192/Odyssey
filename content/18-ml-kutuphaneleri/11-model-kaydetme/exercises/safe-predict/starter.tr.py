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
def safe_predict(rows):
    new = pd.DataFrame(rows)
    return model.predict_proba(new)[:, 1].round(3).tolist()

rows = [{"income": 0.5, "age": -1.0, "score": 1.2, "visits": 0.3},
        {"visits": -0.7, "score": 0.0, "age": 1.5, "income": -0.2}]
print(safe_predict(rows))
