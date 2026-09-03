import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("cars.csv")
X = df[["age", "km", "engine"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

fill_value = X_train["engine"].mean()
print(round(fill_value, 3), round(df["engine"].mean(), 3))

X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})
print(int(X_train.isna().sum().sum()), int(X_test.isna().sum().sum()))

model = LinearRegression()
model.fit(X_train, y_train)
print(round(mean_absolute_error(y_test, model.predict(X_test)), 2))
