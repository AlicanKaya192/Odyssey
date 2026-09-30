import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
cuts = [pd.Timestamp("2024-01-30") + pd.Timedelta(days=56 * i) for i in range(6)]


def plain(train, test):
    fit = ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
    return fit.forecast(28).to_numpy()


def with_exog(train, test):
    # Model exog ile; gelecek tablosunda temp_c = egitimden mevsim normali.
    pass


# Iki yontem, 6 deney: her deneyin MAE'si.


# Her yontem: ad, ortalama MAE, en kotu deney.


# Dis degiskenli modelin kazandigi deney sayisi ve becerisi.
