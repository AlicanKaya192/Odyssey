import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

from sklearn.tree import export_text

model = DecisionTreeClassifier(max_depth=2, random_state=42)
model.fit(X_train, y_train)

print(export_text(model, feature_names=list(X.columns)))
print(X.columns[model.tree_.feature[0]],
      round(float(model.tree_.threshold[0]), 2))
print(int(model.get_n_leaves()), int(model.get_depth()))
