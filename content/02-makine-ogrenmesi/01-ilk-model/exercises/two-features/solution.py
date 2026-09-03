import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.read_csv("homes.csv")
X = df[["area", "age"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
model_mae = mean_absolute_error(y_test, model.predict(X_test))

print(round(model.coef_[0], 2), round(model.coef_[1], 2))
print(round(model_mae, 2))
print("better" if model_mae < 18.5 else "worse")
