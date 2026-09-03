import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("homes.csv")
X = df[["area"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

plt.scatter(X_test, y_test)
plt.plot(X_test, prediction, color="red")
plt.xlabel("area")
plt.ylabel("price")
plt.title("Area and price")
plt.savefig("chart.png")

print(round(r2_score(y_test, prediction), 3))
