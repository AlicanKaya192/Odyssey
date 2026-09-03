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

from sklearn.metrics import accuracy_score

most_common = y_train.mode()[0]
baseline = accuracy_score(y_test, [most_common] * len(y_test))
accuracy = accuracy_score(y_test, prediction)

print(len(X_train), len(X_test))
print(round(baseline, 3), round(accuracy, 3))
print("better" if accuracy > baseline else "worse")
