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
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score)

y = df["readmitted"]


def run(numeric):
    X = df[numeric + text]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    pipe = Pipeline([
        ("prepare", make_preprocessor(numeric)),
        ("model", LogisticRegression(max_iter=1000)),
    ])
    pipe.fit(X_train, y_train)
    prediction = pipe.predict(X_test)
    score = accuracy_score(y_test, prediction)
    print(round(score, 3),
          round(precision_score(y_test, prediction, zero_division=0), 3),
          round(recall_score(y_test, prediction, zero_division=0), 3))
    return score, confusion_matrix(y_test, prediction)


leaky_score, matrix = run(["age", "bmi", "visits", "followup_calls"])
print(matrix)
print(int(matrix[0][1] + matrix[1][0]))

means = df.groupby("readmitted")["followup_calls"].mean().round(2)
print({int(key): float(value) for key, value in means.items()})

clean_score, _ = run(["age", "bmi", "visits"])
print(round(leaky_score - clean_score, 3))
