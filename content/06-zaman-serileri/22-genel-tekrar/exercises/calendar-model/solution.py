import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
weather = pd.read_csv("weather.csv", index_col="date", parse_dates=True)
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]
holidays = pd.to_datetime(pd.read_csv("holidays.csv")["date"])
start = y.index[0]


def features(index):
    x = pd.DataFrame(index=index)
    x["t"] = (index - start).days.to_numpy()
    for day in range(1, 7):
        x[f"d{day}"] = (index.dayofweek == day).astype(float)
    angle = 2 * np.pi * index.dayofyear.to_numpy() / 365.25
    x["s1"], x["c1"] = np.sin(angle), np.cos(angle)
    x["s2"], x["c2"] = np.sin(2 * angle), np.cos(2 * angle)
    x["holiday"] = index.isin(holidays).astype(float)
    return x


def backtest(forecast):
    scores = []
    for cut in cuts:
        train = y.loc[:cut]
        test = y.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        error = test.to_numpy() - forecast(train, test.index)
        scores.append(float(np.abs(error).mean()))
    return round(float(np.mean(scores)), 1), round(max(scores), 1)


def log_model(train, index):
    model = LinearRegression().fit(features(train.index), np.log(train))
    return np.exp(model.predict(features(index)))


def level_model(train, index):
    model = LinearRegression().fit(features(train.index), train)
    return model.predict(features(index))


def weather_model(train, index):
    model = LinearRegression().fit(features(train.index).join(weather), np.log(train))
    return np.exp(model.predict(features(index).join(weather)))


print(backtest(log_model))
print(backtest(level_model))
print(backtest(weather_model))

table = features(y.index).join(weather)
model = LinearRegression().fit(table, np.log(y))
effect = dict(zip(table.columns, np.exp(model.coef_)))
print(round(float(effect["rain"]), 2), round(float(effect["holiday"]), 2))

print(round((1 - backtest(log_model)[0] / 86.9) * 100))
