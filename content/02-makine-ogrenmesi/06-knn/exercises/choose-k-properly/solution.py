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
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

records = []
for k in (1, 3, 5, 7, 9, 15, 25):
    scores = cross_val_score(KNeighborsClassifier(n_neighbors=k),
                             X_train_scaled, y_train, cv=skf,
                             scoring="accuracy")
    mean = float(scores.mean())
    spread = float(scores.std())
    records.append((k, mean, spread))
    print(k, round(mean, 3), round(spread, 3))

best = max(records, key=lambda row: row[1])
limit = best[1] - best[2]
robust = max(k for k, mean, _ in records if mean >= limit)

for k in (best[0], robust):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train_scaled, y_train)
    print(k, round(accuracy_score(y_test, model.predict(X_test_scaled)), 3))
