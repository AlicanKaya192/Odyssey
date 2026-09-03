import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=2, random_state=42)
tree.fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=200, random_state=42)
forest.fit(X_train, y_train)

for name, model in (("tree", tree), ("forest", forest)):
    values = [round(float(value), 3) for value in model.feature_importances_]
    print(name, *values)

tree_zeros = sum(1 for value in tree.feature_importances_ if value == 0)
forest_zeros = sum(1 for value in forest.feature_importances_ if value == 0)
print(tree_zeros, forest_zeros)
