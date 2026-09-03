import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

tree_scores = []
forest_scores = []
thresholds = []

for seed in range(6):
    sample = X_train.sample(frac=0.9, random_state=seed)
    labels = y_train.loc[sample.index]

    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    tree.fit(sample, labels)
    forest = RandomForestClassifier(n_estimators=200, random_state=42)
    forest.fit(sample, labels)

    tree_scores.append(round(accuracy_score(y_test, tree.predict(X_test)), 3))
    forest_scores.append(
        round(accuracy_score(y_test, forest.predict(X_test)), 3))
    thresholds.append(round(float(tree.tree_.threshold[0]), 1))

print(tree_scores)
print(forest_scores)
print(thresholds)
print(round(max(tree_scores) - min(tree_scores), 2),
      round(max(forest_scores) - min(forest_scores), 2))
