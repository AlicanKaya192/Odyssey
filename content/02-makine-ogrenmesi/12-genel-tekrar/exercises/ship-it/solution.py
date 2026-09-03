import joblib
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("patients.csv")
text = ["sex", "region", "smoker"]


def make_preprocessor(numeric):
    return ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]), text),
    ])

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

numeric = ["age", "bmi", "visits"]
X = df[numeric + text]
y = df["readmitted"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

pipe = Pipeline([
    ("prepare", make_preprocessor(numeric)),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
])

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = {
    "model__C": [0.01, 0.1, 1, 10],
    "prepare__num__impute__strategy": ["median", "mean"],
}
search = GridSearchCV(pipe, grid, cv=folds, scoring="average_precision")
search.fit(X_train, y_train)
print(search.best_params_["model__C"],
      search.best_params_["prepare__num__impute__strategy"],
      round(float(search.best_score_), 3))

joblib.dump(search.best_estimator_, "model.joblib")
print(Path("model.joblib").stat().st_size > 1000)

loaded = joblib.load("model.joblib")
probability = loaded.predict_proba(X_test)[:, 1]
print(round(average_precision_score(y_test, probability), 3))

new = pd.DataFrame([
    {"age": 72, "sex": "male", "region": "south", "bmi": 34.5,
     "visits": 5, "smoker": "yes"},
    {"age": 29, "sex": "female", "region": None, "bmi": None,
     "visits": 0, "smoker": "no"},
    {"age": 58, "sex": "female", "region": "north", "bmi": 26.0,
     "visits": 2, "smoker": "no"},
])
risk = loaded.predict_proba(new)[:, 1]
print([round(float(value), 3) for value in risk])
print([int(value) for value in (risk >= 0.3)])
