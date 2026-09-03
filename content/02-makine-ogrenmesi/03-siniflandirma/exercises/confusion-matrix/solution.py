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

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, prediction)
tn, fp, fn, tp = cm.ravel()

print(cm.tolist())
print(int(tn), int(fp), int(fn), int(tp))
print(round((tn + tp) / len(y_test), 3))
print("FP" if fp > fn else "FN")
