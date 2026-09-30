import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"].asfreq("D")
anomaly = t - t.groupby(t.index.dayofyear).transform("mean")

train = anomaly.loc[:"2023"]
fit = ARIMA(train, order=(1, 0, 0)).fit()

phi = float(fit.params["ar.L1"])
print(round(phi, 2))

last = float(train.iloc[-1])
print(round(last, 2), [round(float(v), 2) for v in fit.forecast(5)])
print([round(last * phi ** step, 2) for step in range(1, 6)])

actual = anomaly.loc["2024"]
previous = anomaly.shift(1).loc["2024"]
mean_error = float(actual.abs().mean())
naive_error = float((actual - previous).abs().mean())
ar_error = float((actual - phi * previous).abs().mean())
print(round(mean_error, 2), round(naive_error, 2), round(ar_error, 2))
