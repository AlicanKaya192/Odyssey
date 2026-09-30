import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

growth = train.loc["2023"].sum() / train.loc["2022"].sum()
bar = pd.Series(train.loc["2023"].to_numpy() * growth, index=test.index)
bar_mae = float((test - bar).abs().mean())
print(round(bar_mae, 2))

settings = {
    "add-add": ("add", "add"),
    "add-mul": ("add", "mul"),
    "mul-mul": ("mul", "mul"),
}

fits = {}
scores = {}
for name, (trend, seasonal) in settings.items():
    fit = ExponentialSmoothing(train, trend=trend, seasonal=seasonal, seasonal_periods=12).fit()
    error = (test - fit.forecast(12)).abs()
    fits[name] = fit
    scores[name] = float(error.mean())
    print(name, round(scores[name], 2), round(float((error / test).mean() * 100), 1))

best = min(scores, key=scores.get)
print(round(1 - scores[best] / bar_mae, 2))

keys = ("smoothing_level", "smoothing_trend", "smoothing_seasonal")
print([abs(round(float(fits[best].params[key]), 2)) for key in keys])

month = "2024-08-01"
print(round(float(fits[best].forecast(12).loc[month])), int(test.loc[month]))
