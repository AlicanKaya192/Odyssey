import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.get_dummies(pd.read_csv("cars.csv").dropna(),
                    columns=["fuel", "gearbox"])
X = df.drop(columns=["price"])
y = df["price"]

results = []
for seed in range(5):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed)
    model = LinearRegression()
    model.fit(X_train, y_train)
    error = mean_absolute_error(y_test, model.predict(X_test))
    results.append(round(error, 2))

print(results)
print(min(results), max(results), round(max(results) - min(results), 2))
