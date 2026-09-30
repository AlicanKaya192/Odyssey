import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
columns = ["promo", "holiday", "temp_c"]

# Dis degiskensiz model.


# Dis degiskenli model.


# Iki modelin AIC'si.


# Uc dis degiskenin katsayisi.


# Uc katsayinin guven araligi (alt, ust).


# Iki modelin kalinti standart sapmasi.
