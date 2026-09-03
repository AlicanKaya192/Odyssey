import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("students.csv")
X = df[["hours", "prev_score", "attendance"]]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
prediction = model.predict(X_test)

from sklearn.metrics import (confusion_matrix, f1_score, precision_score,
                             recall_score)

tn, fp, fn, tp = confusion_matrix(y_test, prediction).ravel()

precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

print(round(precision, 3))
print(round(recall, 3))
print(round(f1, 3))
print(round(precision_score(y_test, prediction), 3),
      round(recall_score(y_test, prediction), 3),
      round(f1_score(y_test, prediction), 3))
