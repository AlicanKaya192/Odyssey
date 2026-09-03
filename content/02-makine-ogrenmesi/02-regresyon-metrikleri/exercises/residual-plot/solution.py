import matplotlib.pyplot as plt
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

residuals = y_train - model.predict(X_train)
ages = df.loc[X_train.index, "age"]

plt.scatter(ages, residuals)
plt.axhline(0, color="red")
plt.xlabel("age")
plt.ylabel("residual")
plt.title("Residuals against age")
plt.savefig("chart.png")

print(round(residuals.corr(ages), 3))
