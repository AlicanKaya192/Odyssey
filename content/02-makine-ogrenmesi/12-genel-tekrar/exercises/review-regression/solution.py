import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error, r2_score,
                             root_mean_squared_error)
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv("cars.csv")
numeric = ["age", "km", "engine"]
text = ["fuel", "gearbox"]
X = df[numeric + text]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)


def make_preprocessor():
    return ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), text),
    ])


baseline = [y_train.mean()] * len(y_test)
print(round(mean_absolute_error(y_test, baseline), 1),
      round(root_mean_squared_error(y_test, baseline), 1),
      round(r2_score(y_test, baseline), 3))

folds = KFold(n_splits=5, shuffle=True, random_state=42)
models = [
    ("linear", LinearRegression()),
    ("tree", DecisionTreeRegressor(max_depth=3, random_state=42)),
    ("forest", RandomForestRegressor(n_estimators=200, random_state=42)),
]

rows = []
for name, model in models:
    pipe = Pipeline([("prepare", make_preprocessor()), ("model", model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=folds,
                             scoring="neg_mean_absolute_error")
    pipe.fit(X_train, y_train)
    prediction = pipe.predict(X_test)
    cv_error = float(-scores.mean())
    test_error = mean_absolute_error(y_test, prediction)
    rows.append((name, cv_error, test_error))
    print(name, round(cv_error, 1), round(float(scores.std()), 1),
          round(test_error, 1), round(r2_score(y_test, prediction), 3))

best_cv = min(rows, key=lambda row: row[1])[0]
best_test = min(rows, key=lambda row: row[2])[0]
print(best_cv, best_test)
