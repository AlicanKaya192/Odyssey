import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = [
    ("tree", DecisionTreeClassifier(max_depth=2, random_state=42)),
    ("forest", RandomForestClassifier(n_estimators=200, random_state=42)),
    ("boosting", GradientBoostingClassifier(random_state=42)),
]

baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))
print(round(baseline, 3))

rows = []
for name, model in models:
    model.fit(X_train, y_train)
    test_score = accuracy_score(y_test, model.predict(X_test))
    scores = cross_val_score(model, X_train, y_train, cv=skf)
    rows.append((name, test_score, float(scores.mean())))
    print(name, round(test_score, 3),
          round(float(scores.mean()), 3), round(float(scores.std()), 3))

best_test = max(rows, key=lambda row: row[1])[0]
best_cv = max(rows, key=lambda row: row[2])[0]
print(best_test, best_cv)
print("different" if best_test != best_cv else "same")
