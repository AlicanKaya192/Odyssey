import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

pairs = list(zip(X.columns, model.feature_importances_))
for name, value in pairs:
    print(name, round(float(value), 3))
print(max(pairs, key=lambda row: row[1])[0])

fig, ax = plt.subplots(figsize=(11, 5))
plot_tree(model, feature_names=list(X.columns),
          class_names=["stays", "leaves"],
          filled=True, rounded=True, fontsize=9, ax=ax)
fig.tight_layout()
fig.savefig("chart.png")
