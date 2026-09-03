import matplotlib.pyplot as plt
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
thresholds = [round(0.05 * i, 2) for i in range(1, 20)]

precisions = []
recalls = []
best = None

for t in thresholds:
    guess = (probability >= t).astype(int)
    p = precision_score(y_test, guess, zero_division=0)
    r = recall_score(y_test, guess)
    precisions.append(p)
    recalls.append(r)
    if r >= 0.9:
        best = t

plt.plot(thresholds, precisions, label="precision")
plt.plot(thresholds, recalls, label="recall")
plt.xlabel("threshold")
plt.ylabel("score")
plt.title("Precision and recall by threshold")
plt.legend()
plt.savefig("chart.png")

print(best)
