import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]

inside = []
widths = []
for cut in cuts:
    train = s.loc[:cut]
    test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
    fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()
    interval = fit.get_forecast(28).conf_int(alpha=0.05)
    low = interval.iloc[:, 0].to_numpy()
    high = interval.iloc[:, 1].to_numpy()
    actual = test.to_numpy()
    inside.append((actual >= low) & (actual <= high))
    widths.append(float((high - low).mean()))

inside = np.array(inside)
print(round(float(inside.mean()), 3))

by_fold = inside.mean(axis=1)
print([round(float(v), 2) for v in by_fold])

bad = by_fold < 0.8
print([cut.strftime("%Y-%m-%d") for cut, flag in zip(cuts, bad) if flag])

print(round(float(inside[~bad].mean()), 3), round(float(np.mean(widths)), 1))
