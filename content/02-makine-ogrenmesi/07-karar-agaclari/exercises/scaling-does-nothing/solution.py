import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

raw = DecisionTreeClassifier(max_depth=3, random_state=42)
raw.fit(X_train, y_train)
raw_score = accuracy_score(y_test, raw.predict(X_test))

scaler = StandardScaler()
scaler.fit(X_train)
scaled = DecisionTreeClassifier(max_depth=3, random_state=42)
scaled.fit(scaler.transform(X_train), y_train)
scaled_score = accuracy_score(y_test, scaled.predict(scaler.transform(X_test)))

print(round(raw_score, 3), round(scaled_score, 3))
print("same" if round(raw_score, 3) == round(scaled_score, 3) else "different")
print(round(0.92 - 0.64, 2))
