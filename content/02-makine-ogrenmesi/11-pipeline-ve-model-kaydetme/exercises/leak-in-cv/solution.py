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

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

prepared = make_preprocessor().fit_transform(X_train, y_train)
real_count = prepared.shape[1]

rng = np.random.default_rng(7)
noise = rng.normal(0, 1, (len(X_train), 200))
wide = np.hstack([prepared, noise])
print(wide.shape[1])

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

selector = SelectKBest(f_classif, k=15).fit(wide, y_train)
picked = selector.transform(wide)
wrong = cross_val_score(LogisticRegression(max_iter=1000), picked,
                        y_train, cv=folds)
print(round(float(wrong.mean()), 3))

honest = Pipeline([
    ("select", SelectKBest(f_classif, k=15)),
    ("model", LogisticRegression(max_iter=1000)),
])
right = cross_val_score(honest, wide, y_train, cv=folds)
print(round(float(right.mean()), 3))

print(round(float(wrong.mean() - right.mean()), 3))

chosen = selector.get_support(indices=True)
print(int((chosen >= real_count).sum()))
