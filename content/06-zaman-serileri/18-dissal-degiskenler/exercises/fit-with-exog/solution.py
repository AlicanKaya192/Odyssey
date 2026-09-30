import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
columns = ["promo", "holiday", "temp_c"]

plain = ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
fit = ARIMA(train["sales"], exog=train[columns], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()

print(round(float(plain.aic), 1), round(float(fit.aic), 1))

for name in columns:
    print(name, round(float(fit.params[name]), 1))

intervals = fit.conf_int()
for name in columns:
    print(name, round(float(intervals.loc[name, 0]), 1), round(float(intervals.loc[name, 1]), 1))

print(round(float(plain.resid.iloc[8:].std()), 1), round(float(fit.resid.iloc[8:].std()), 1))
