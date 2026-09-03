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
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

print(round(float(y.mean()), 3))
print(len(y_test), int(y_test.sum()))

zeros = [0] * len(y_test)
print(round(accuracy_score(y_test, zeros), 3),
      round(recall_score(y_test, zeros, zero_division=0), 3))

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
prediction = model.predict(X_test_scaled)

print(round(accuracy_score(y_test, prediction), 3),
      round(precision_score(y_test, prediction, zero_division=0), 3),
      round(recall_score(y_test, prediction, zero_division=0), 3),
      round(f1_score(y_test, prediction, zero_division=0), 3))

matrix = confusion_matrix(y_test, prediction)
print(matrix)
print(matrix[1][0])
