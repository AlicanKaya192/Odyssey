import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Mevsimsel fark.


# Bandi asan gecikme sayisi: seri, d7 (21 gecikme).


# d7'nin ACF'si: 1, 7 ve 14. gecikme.


# d7'de mutlak degeri en buyuk gecikme ve degeri.


# d7'nin korelogramini chart.png olarak kaydet.
