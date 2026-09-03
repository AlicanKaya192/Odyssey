import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

scores = {}
for count in (1, 5, 25, 100, 300):
    model = RandomForestClassifier(n_estimators=count, random_state=42)
    model.fit(X_train, y_train)
    train_score = accuracy_score(y_train, model.predict(X_train))
    test_score = accuracy_score(y_test, model.predict(X_test))
    scores[count] = round(test_score, 3)
    print(count, round(train_score, 3), round(test_score, 3))

print("same" if scores[25] == scores[300] else "different")
