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

mean = y_test.mean()
ss_res = sum((a - p) ** 2 for a, p in zip(y_test, prediction))
ss_tot = sum((a - mean) ** 2 for a in y_test)
r2 = 1 - ss_res / ss_tot

print(round(ss_res, 2))
print(round(ss_tot, 2))
print(round(r2, 3), round(r2_score(y_test, prediction), 3))
