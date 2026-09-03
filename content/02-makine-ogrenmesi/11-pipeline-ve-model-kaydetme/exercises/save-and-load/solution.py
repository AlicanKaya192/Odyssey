import joblib
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("subscribers.csv")
X = df.drop(columns="churn")
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

numeric = ["tenure", "monthly", "support"]
text = ["city", "plan"]


def make_preprocessor():
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

pipe = Pipeline([
    ("prepare", make_preprocessor()),
    ("model", LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)

joblib.dump(pipe, "model.joblib")
print(Path("model.joblib").stat().st_size > 1000)

loaded = joblib.load("model.joblib")
print(bool((loaded.predict(X_test) == pipe.predict(X_test)).all()))

new = pd.DataFrame([
    {"city": "Bursa", "plan": "basic", "tenure": 3,
     "monthly": 140.0, "support": 4},
    {"city": "Izmir", "plan": "pro", "tenure": 48,
     "monthly": 45.0, "support": 0},
    {"city": None, "plan": "plus", "tenure": 20,
     "monthly": None, "support": 1},
])

print(loaded.predict(new).tolist())
print([round(float(value), 3) for value in loaded.predict_proba(new)[:, 1]])
