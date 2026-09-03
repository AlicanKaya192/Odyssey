import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)
tree_score = accuracy_score(y_test, tree.predict(X_test))

scaler = StandardScaler()
scaler.fit(X_train)
knn = KNeighborsClassifier(n_neighbors=25)
knn.fit(scaler.transform(X_train), y_train)
knn_score = accuracy_score(y_test, knn.predict(scaler.transform(X_test)))

print(round(baseline, 3), round(tree_score, 3), round(knn_score, 3))
print("better" if tree_score > baseline else "worse")
print("knn" if knn_score > tree_score else "tree")
