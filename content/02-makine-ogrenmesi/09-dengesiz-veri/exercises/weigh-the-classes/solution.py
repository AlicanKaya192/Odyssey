import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour", "attempts"]]
y = df["fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)

models = [
    ("logreg", LogisticRegression(max_iter=1000), True),
    ("logreg-bal",
     LogisticRegression(max_iter=1000, class_weight="balanced"), True),
    ("forest",
     RandomForestClassifier(n_estimators=200, random_state=42), False),
    ("forest-bal",
     RandomForestClassifier(n_estimators=200, class_weight="balanced",
                            random_state=42), False),
]

recalls = {}
for name, model, scaled in models:
    if scaled:
        model.fit(X_train_scaled, y_train)
        prediction = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
    recall = recall_score(y_test, prediction, zero_division=0)
    recalls[name] = recall
    print(name, round(accuracy_score(y_test, prediction), 3),
          round(precision_score(y_test, prediction, zero_division=0), 3),
          round(recall, 3),
          round(f1_score(y_test, prediction, zero_division=0), 3))

print(round(recalls["logreg-bal"] - recalls["logreg"], 3))
