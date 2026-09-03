import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("cars.csv")
features = df[["age", "km", "engine", "fuel", "gearbox"]]
y = df["price"]

encoded = pd.get_dummies(features, columns=["fuel", "gearbox"])
print(len(encoded.columns))
print(sorted(encoded.columns.tolist()))

X_train, X_test, y_train, y_test = train_test_split(
    encoded, y, test_size=0.25, random_state=42)

fill_value = X_train["engine"].mean()
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})

model = LinearRegression()
model.fit(X_train, y_train)
mae = mean_absolute_error(y_test, model.predict(X_test))

print(round(mae, 2))
print("better" if mae < 32.58 else "worse")
