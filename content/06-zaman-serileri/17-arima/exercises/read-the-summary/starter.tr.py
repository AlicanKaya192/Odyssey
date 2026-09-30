import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]

# (1,1,1)(0,1,1,7) modeli.


# sigma2 disindaki katsayilar: ad, deger, p-degeri.


# p-degeri 0.05'in ustunde olan katsayilar.


# (0,1,1)(0,1,1,7) modeli; iki modelin AIC'si.


# Iki modelin kalinti standart sapmasi.
