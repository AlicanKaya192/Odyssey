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

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = [
    ("logreg", LogisticRegression(max_iter=1000)),
    ("forest", RandomForestClassifier(n_estimators=200, random_state=42)),
]

rows = []
for name, model in models:
    pipe = Pipeline([("prepare", make_preprocessor()), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=folds)
    pipe.fit(X_train, y_train)
    test_score = accuracy_score(y_test, pipe.predict(X_test))
    rows.append((name, float(scores.mean()), test_score))
    print(name, round(float(scores.mean()), 3), round(float(scores.std()), 3),
          round(test_score, 3))

best_cv = max(rows, key=lambda row: row[1])[0]
best_test = max(rows, key=lambda row: row[2])[0]
print(best_cv, best_test)
