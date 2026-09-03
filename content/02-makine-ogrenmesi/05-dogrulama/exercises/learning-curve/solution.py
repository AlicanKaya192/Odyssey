import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

df = pd.get_dummies(pd.read_csv("cars.csv").dropna(),
                    columns=["fuel", "gearbox"])
X = df.drop(columns=["price"])
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

sizes = [10, 20, 30, 45, 60, 79]
train_errors = []
test_errors = []

for n in sizes:
    model = LinearRegression()
    model.fit(X_train[:n], y_train[:n])
    train_error = mean_absolute_error(y_train[:n], model.predict(X_train[:n]))
    test_error = mean_absolute_error(y_test, model.predict(X_test))
    train_errors.append(train_error)
    test_errors.append(test_error)
    print(n, round(train_error, 2), round(test_error, 2))

plt.plot(sizes, train_errors, label="training")
plt.plot(sizes, test_errors, label="test")
plt.xlabel("training size")
plt.ylabel("MAE")
plt.title("Learning curve")
plt.legend()
plt.savefig("chart.png")

gap = abs(test_errors[-1] - train_errors[-1])
print("no" if gap < 1 else "yes")
