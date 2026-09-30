import pandas as pd
from sklearn.linear_model import LinearRegression

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    X = pd.DataFrame(index=y.index)
    for k in (1, 2, 7, 14):
        X[f"lag{k}"] = y.shift(k)
    X["mean7"] = y.shift(1).rolling(7).mean()
    X["mean28"] = y.shift(1).rolling(28).mean()
    X["dow"] = y.index.dayofweek
    X["month"] = y.index.month
    return X


table = features(s).join(s.rename("y")).dropna()
columns = [c for c in table.columns if c != "y"]
train, test = table.loc[:"2023"], table.loc["2024"]

model = LinearRegression().fit(train[columns], train["y"])
predicted = model.predict(test[columns])


def mae(actual, forecast):
    return float((actual - forecast).abs().mean())


naive = mae(test["y"], test["lag1"])
snaive = mae(test["y"], test["lag7"])
linear = mae(test["y"], predicted)
print(round(naive, 2), round(snaive, 2), round(linear, 2))

train_error = mae(train["y"], model.predict(train[columns]))
print(round(train_error, 2), round(linear, 2))

print(round(1 - linear / snaive, 2))

pairs = sorted(zip(columns, model.coef_), key=lambda pair: abs(pair[1]), reverse=True)
for name, value in pairs:
    print(name, round(float(value), 2))
