import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()


def outside(x, nlags=20):
    # Bandi asan gecikme numaralari (gecikme 0 haric).
    pass


# Gunluk degisim icin bant (uc ondalik).


# Gunluk degisimde bandi asan gecikmeler.


# Fiyatta bandi asan gecikme sayisi.


# Fiyatin ACF'si: 1, 10 ve 20. gecikme.
