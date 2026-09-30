import numpy as np
import pandas as pd

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def backtest(forecast):
    scores = []
    for cut in cuts:
        train = y.loc[:cut]
        test = y.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        error = test.to_numpy() - forecast(train, test.index)
        scores.append(float(np.abs(error).mean()))
    return round(float(np.mean(scores)), 1), round(max(scores), 1)


def naive(train, index):
    return np.full(len(index), train.iloc[-1])


def seasonal_naive(train, index):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(len(index))])


def week_mean(train, index):
    recent = train.iloc[-28:]
    profile = recent.groupby(recent.index.dayofweek).mean()
    return profile.reindex(index.dayofweek).to_numpy()


print(backtest(naive))
print(backtest(seasonal_naive))
print(backtest(week_mean))

level = float(y.loc["2024-01-03":].mean())
print(round(level), round(backtest(seasonal_naive)[0] / level * 100))
