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

from sklearn.metrics import precision_score, recall_score

probability = model.predict_proba(X_test)[:, 1]

for t in (0.3, 0.5, 0.7):
    guess = (probability >= t).astype(int)
    print(t,
          round(precision_score(y_test, guess, zero_division=0), 3),
          round(recall_score(y_test, guess), 3))
