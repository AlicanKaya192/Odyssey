import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)
load = load["load_mw"]

# ACF, 200 gecikme.


# 2-30 arasinda en yuksek: gecikme ve deger.


# 2-30 arasinda en dusuk: gecikme ve deger.


# 100-200 arasinda en yuksek: gecikme ve deger.


# 24'un katlarindaki ACF (24, 48, ..., 168).
