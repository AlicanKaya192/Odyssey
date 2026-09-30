import warnings

warnings.simplefilter("ignore")    # KPSS'in tablo disi p-degeri uyarisi

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]

# Dort seri: level, diff, diff12, log diff12 (sozluk).


# Her biri icin: ad, ADF p, KPSS p.


# Son seride kaybedilen satir sayisi ve standart sapma.


# Gereksiz bir fark daha: standart sapma.
