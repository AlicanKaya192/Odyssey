import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

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

print(int(train["y"].max()), int(test["y"].max()))

model = HistGradientBoostingRegressor(random_state=0).fit(train[columns], train["y"])
level = pd.Series(model.predict(test[columns]), index=test.index)
print(round(float(level.max()), 1))


def errors(forecast):
    error = (test["y"] - forecast).abs()
    return round(float(error.mean()), 2), round(float(error.loc["2024-12"].mean()), 2)


print(*errors(level))

relative = table[columns].drop(columns=["lag7"]).copy()
for name in ("lag1", "lag2", "lag14", "mean7", "mean28"):
    relative[name] = relative[name] - table["lag7"]
target = table["y"] - table["lag7"]

model = HistGradientBoostingRegressor(random_state=0)
model.fit(relative.loc[:"2023"], target.loc[:"2023"])
change = pd.Series(model.predict(relative.loc["2024"]), index=test.index)
difference = change + test["lag7"]

print(*errors(difference))
print(round(float(difference.max()), 1))
