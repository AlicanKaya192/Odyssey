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
from sklearn.metrics import (confusion_matrix, f1_score, precision_score,
                             recall_score)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
probability = model.predict_proba(X_test_scaled)[:, 1]

scores = []
for threshold in (0.5, 0.4, 0.3, 0.2, 0.1, 0.05):
    prediction = (probability >= threshold).astype(int)
    score = f1_score(y_test, prediction, zero_division=0)
    caught = confusion_matrix(y_test, prediction)[1][1]
    scores.append((threshold, score))
    print(threshold,
          round(precision_score(y_test, prediction, zero_division=0), 3),
          round(recall_score(y_test, prediction, zero_division=0), 3),
          round(score, 3), caught)

best = max(scores, key=lambda row: row[1])
print(best[0], round(best[1], 3))
