import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# Cita: 2023 x buyume orani; MAE.


# Uc model: add-add, add-mul, mul-mul.


# Her biri icin: ad, MAE, yuzde hata.


# En iyi modelin citaya gore becerisi.


# En iyi modelin uc katsayisi.


# Agustos 2024: en iyi modelin tahmini ve gercek.
