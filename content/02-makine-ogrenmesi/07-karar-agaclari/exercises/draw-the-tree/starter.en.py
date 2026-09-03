import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

# Import matplotlib.pyplot and plot_tree as well.


# Train the tree with max_depth=2 (random_state=42).


# Print each column's importance: the name and the value (three decimals).


# Print the name of the most important column.


# Draw the tree: pass feature_names, class names "stays" and "leaves",
# and colour the boxes.


# Save it as chart.png.
