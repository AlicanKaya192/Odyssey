import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]
fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()

# get_forecast(28): tahmin ve %95 aralik.


# Ilk gun: tahmin, alt uc, ust uc, gercek.


# Aralik genisligi: 1., 7., 14., 28. gun.


# Kapsama: %95 ve %80.


# %95 araligin disinda kalan gunler.


# Grafik: gercek, tahmin, fill_between ile bant; chart.png.
