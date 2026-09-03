import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

for depth in (1, 2, 3, 5, 8, None):
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_score = accuracy_score(y_train, model.predict(X_train))
    test_score = accuracy_score(y_test, model.predict(X_test))
    print(depth if depth else "none",
          round(train_score, 3), round(test_score, 3))

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
best_depth = None
best_mean = -1.0

for depth in (1, 2, 3, 5, None):
    scores = cross_val_score(
        DecisionTreeClassifier(max_depth=depth, random_state=42),
        X_train, y_train, cv=skf)
    print(depth if depth else "none",
          round(float(scores.mean()), 3), round(float(scores.std()), 3))
    if scores.mean() > best_mean:
        best_mean = scores.mean()
        best_depth = depth

print(best_depth)
