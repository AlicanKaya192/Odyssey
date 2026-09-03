import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

counts = [10, 25, 50, 100, 200]
oob_scores = []
test_scores = []

for count in counts:
    model = RandomForestClassifier(n_estimators=count, oob_score=True,
                                   random_state=42)
    model.fit(X_train, y_train)
    oob = float(model.oob_score_)
    test = accuracy_score(y_test, model.predict(X_test))
    oob_scores.append(oob)
    test_scores.append(test)
    print(count, round(oob, 3), round(test, 3))

plt.plot(counts, oob_scores, label="oob", marker="o")
plt.plot(counts, test_scores, label="test", marker="o")
plt.xlabel("trees")
plt.ylabel("accuracy")
plt.title("Out-of-bag against test")
plt.legend()
plt.savefig("chart.png")

print(round(abs(oob_scores[-1] - test_scores[-1]), 3))
