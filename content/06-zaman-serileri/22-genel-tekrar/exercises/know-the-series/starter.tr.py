import pandas as pd
from statsmodels.tsa.stattools import adfuller

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
weather = pd.read_csv("weather.csv", index_col="date", parse_dates=True)

# Yillik toplamlar ve yildan yila yuzde degisim.


# Haftanin gunu ortalamalari; cumartesi / pazartesi.


# En yuksek ve en dusuk ay; oranlari.


# ADF p-degeri: duzey ve birinci fark.


# Yagmurlu / kuru orani; sicaklikla korelasyon.
