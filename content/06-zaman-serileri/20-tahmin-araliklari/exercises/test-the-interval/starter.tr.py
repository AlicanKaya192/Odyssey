import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]

# Her kesimde: model, %95 aralik; icinde mi (28 deger) ve ortalama genislik.


# Toplam kapsama.


# Deney deney kapsama (liste).


# Kapsamasi 0.8'in altinda kalan deneylerin kesim gunleri.


# Onlar cikarilinca kapsama ve ortalama genislik.
