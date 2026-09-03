import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.get_dummies(pd.read_csv("cars.csv").dropna(),
                    columns=["fuel", "gearbox"])
X = df.drop(columns=["price"])
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor

for name, depth in (("simple", 1), ("complex", None)):
    model = DecisionTreeRegressor(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_error = mean_absolute_error(y_train, model.predict(X_train))
    test_error = mean_absolute_error(y_test, model.predict(X_test))
    gap = test_error - train_error

    if gap > 20:
        label = "overfit"
    elif train_error > 50:
        label = "underfit"
    else:
        label = "ok"

    print(name, round(train_error, 2), round(test_error, 2), label)
