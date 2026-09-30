import pandas as pd
from pandas.tseries.offsets import BDay, CustomBusinessDay

orders = ["2024-03-08", "2024-04-09", "2024-06-14"]

# Tatil tarihlerini oku.


# Tatilleri bilen is gunu ofseti.


# 2024'teki calisma gunu sayisi: tatilsiz ve tatilli.


# Her siparis: BDay(3) ve 3 * workday ile teslim gunu.
