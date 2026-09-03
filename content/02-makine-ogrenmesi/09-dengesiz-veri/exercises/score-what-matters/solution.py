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

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
spreads = []

for scoring in ("accuracy", "recall", "f1", "roc_auc", "average_precision"):
    scores = cross_val_score(LogisticRegression(max_iter=1000),
                             X_train_scaled, y_train, cv=folds,
                             scoring=scoring)
    spread = float(scores.std())
    spreads.append((scoring, spread))
    print(scoring, round(float(scores.mean()), 3), round(spread, 3))

narrowest = min(spreads, key=lambda row: row[1])[0]
widest = max(spreads, key=lambda row: row[1])[0]
print(narrowest, widest)
