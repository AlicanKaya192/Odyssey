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
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

print(df.isna().sum().to_dict())
print(round(float(df["readmitted"].mean()), 3))

numeric = ["age", "bmi", "visits"]
X = df[numeric + text]
y = df["readmitted"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
print(len(y_test), int(y_test.sum()))

print(round(accuracy_score(y_test, [0] * len(y_test)), 3))


def report(weight):
    pipe = Pipeline([
        ("prepare", make_preprocessor(numeric)),
        ("model", LogisticRegression(max_iter=1000, class_weight=weight)),
    ])
    pipe.fit(X_train, y_train)
    prediction = pipe.predict(X_test)
    print(round(accuracy_score(y_test, prediction), 3),
          round(precision_score(y_test, prediction, zero_division=0), 3),
          round(recall_score(y_test, prediction, zero_division=0), 3),
          round(f1_score(y_test, prediction, zero_division=0), 3))
    return prediction


plain = report(None)
print(confusion_matrix(y_test, plain))
report("balanced")
