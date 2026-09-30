import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

annual = p.resample("YS").sum()
train, test = annual.iloc[:-2], annual.iloc[-2:]

models = {
    "flat": ExponentialSmoothing(train).fit(),
    "additive": ExponentialSmoothing(train, trend="add").fit(),
    "multiplicative": ExponentialSmoothing(train, trend="mul").fit(),
}

for name, fit in models.items():
    forecast = fit.forecast(2)
    error = float((test - forecast).abs().mean())
    print(name, [round(float(v)) for v in forecast], round(error, 1))

print([int(v) for v in test])
print(round(float(train.pct_change().mean() * 100), 1))
