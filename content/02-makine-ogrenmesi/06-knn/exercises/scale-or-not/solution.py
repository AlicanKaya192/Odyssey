import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.metrics import accuracy_score

baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))

raw = KNeighborsClassifier(n_neighbors=5)
raw.fit(X_train, y_train)
raw_score = accuracy_score(y_test, raw.predict(X_test))

scaled = KNeighborsClassifier(n_neighbors=5)
scaled.fit(X_train_scaled, y_train)
scaled_score = accuracy_score(y_test, scaled.predict(X_test_scaled))

print(len(X_train), len(X_test))
print(round(baseline, 3))
print(round(raw_score, 3), round(scaled_score, 3))
print("worse" if raw_score < baseline else "better")
