import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
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


def log_model(train, index):
    model = LinearRegression().fit(features(train.index), np.log(train))
    return np.exp(model.predict(features(index)))


errors = []
for cut in cuts:
    train = y.loc[:cut]
    test = y.loc[cut + pd.Timedelta(days=1):].iloc[:28]
    errors.append(test.to_numpy() / log_model(train, test.index) - 1)
errors = np.array(errors)

low, high = np.quantile(errors, [0.10, 0.90])
print(round(float(errors.mean()), 3), round(float(low), 3), round(float(high), 3))

coverage = []
for i in range(len(errors)):
    rest = np.delete(errors, i, axis=0)
    a, b = np.quantile(rest, [0.10, 0.90])
    coverage.append(float(((errors[i] >= a) & (errors[i] <= b)).mean()))
print(round(float(np.mean(coverage)), 3))

future = pd.date_range("2025-01-01", periods=28, freq="D")
point = log_model(y, future)
print(round(float(point.sum())))

print(round(float(point[0])), round(float(point[0] * (1 + low))),
      round(float(point[0] * (1 + high))))

past = y.iloc[-42:]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(past.index, past.values, color="gray", label="actual")
ax.plot(future, point, label="forecast")
ax.fill_between(future, point * (1 + low), point * (1 + high), alpha=0.2, label="80%")
ax.legend()
fig.savefig("chart.png")
