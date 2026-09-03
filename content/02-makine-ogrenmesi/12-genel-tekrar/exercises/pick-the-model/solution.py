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

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

numeric = ["age", "bmi", "visits"]
X = df[numeric + text]
y = df["readmitted"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = [
    ("logreg", LogisticRegression(max_iter=1000)),
    ("knn", KNeighborsClassifier(n_neighbors=15)),
    ("forest", RandomForestClassifier(n_estimators=200, random_state=42)),
    ("boosting", GradientBoostingClassifier(random_state=42)),
]

rows = []
for name, model in models:
    pipe = Pipeline([("prepare", make_preprocessor(numeric)), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=folds,
                             scoring="average_precision")
    pipe.fit(X_train, y_train)
    probability = pipe.predict_proba(X_test)[:, 1]
    rows.append((name, float(scores.mean())))
    print(name, round(float(scores.mean()), 3), round(float(scores.std()), 3),
          round(roc_auc_score(y_test, probability), 3),
          round(average_precision_score(y_test, probability), 3))

print(round(float(y_test.mean()), 3))
print(max(rows, key=lambda row: row[1])[0])
