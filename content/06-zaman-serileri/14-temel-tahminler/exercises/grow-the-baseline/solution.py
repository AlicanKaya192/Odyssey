import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

base = train.loc["2023"].to_numpy()

slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
growth = train.loc["2023"].sum() / train.loc["2022"].sum()
print(round(float(growth), 4))

forecasts = {
    "snaive": pd.Series(base, index=test.index),
    "drift": pd.Series(base + slope * 12, index=test.index),
    "growth": pd.Series(base * growth, index=test.index),
}

scores = {}
for name, fc in forecasts.items():
    error = (test - fc).abs()
    scores[name] = float(error.mean())
    print(name, round(scores[name], 2), round(float((error / test).mean() * 100), 1))

print(round(1 - scores["growth"] / scores["snaive"], 2))

month = "2024-08-01"
print(int(test.loc[month]), *[round(float(fc.loc[month])) for fc in forecasts.values()])
