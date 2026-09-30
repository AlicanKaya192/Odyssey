import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
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

models = {
    "linear": LinearRegression(),
    "forest": RandomForestRegressor(n_estimators=200, random_state=0),
    "boosting": HistGradientBoostingRegressor(random_state=0),
}


def mae(actual, forecast):
    return float((actual - forecast).abs().mean())


snaive = mae(test["y"], test["lag7"])
winners = []
for name, model in models.items():
    model.fit(train[columns], train["y"])
    train_error = mae(train["y"], model.predict(train[columns]))
    test_error = mae(test["y"], model.predict(test[columns]))
    print(name, round(train_error, 2), round(test_error, 2), round(test_error / train_error, 1))
    if test_error < snaive:
        winners.append(name)

print(winners)
