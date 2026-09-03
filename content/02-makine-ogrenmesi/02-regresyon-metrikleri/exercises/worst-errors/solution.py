import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("homes.csv")
X = df[["area"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

residuals = y_test - prediction
worst = residuals.abs().idxmax()

print(round(residuals.mean(), 2))
print(round(residuals.abs().max(), 2))
print(int(df.loc[worst, "area"]), int(df.loc[worst, "age"]))
print(int((residuals > 0).sum()), int((residuals < 0).sum()))
