import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

annual = p.resample("YS").sum()
train, test = annual.iloc[:-2], annual.iloc[-2:]

# Uc model: flat, additive, multiplicative.


# Her biri icin: ad, iki yillik tahmin (liste), MAE.


# Gercek degerler (liste).


# Egitimde yillik ortalama buyume orani (yuzde).
