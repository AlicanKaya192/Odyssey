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
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold

pipe = Pipeline([
    ("prepare", make_preprocessor()),
    ("model", LogisticRegression(max_iter=1000)),
])

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.01, 0.1, 1, 10],
}

search = GridSearchCV(pipe, grid, cv=folds, scoring="accuracy")
search.fit(X_train, y_train)

for params, mean in zip(search.cv_results_["params"],
                        search.cv_results_["mean_test_score"]):
    print(params["prepare__num__impute__strategy"], params["model__C"],
          round(float(mean), 3))

print(search.best_params_["prepare__num__impute__strategy"],
      search.best_params_["model__C"], round(float(search.best_score_), 3))

plain = Pipeline([
    ("prepare", make_preprocessor()),
    ("model", LogisticRegression(max_iter=1000)),
])
plain.fit(X_train, y_train)
print(round(accuracy_score(y_test, search.predict(X_test)), 3),
      round(accuracy_score(y_test, plain.predict(X_test)), 3))
