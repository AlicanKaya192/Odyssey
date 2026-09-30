import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
test = c.loc["2024-11-01":"2024-11-28"]
columns = ["promo", "holiday", "temp_c"]

fit = ARIMA(train["sales"], exog=train[columns], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()

# Uc gelecek tablosu: actual, last, normal (yalnizca temp_c farkli).


# Her varsayimin sicaklik hatasi.


# Her varsayimla satis tahmini: MAE.


# Durust en iyi MAE eksi hileli MAE.
