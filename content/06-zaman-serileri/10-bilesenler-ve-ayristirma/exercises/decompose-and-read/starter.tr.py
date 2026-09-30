import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Toplamsal ayristirma, period=7.


# Grafigi chart.png olarak kaydet.


# Kalintidaki NaN sayisi ve standart sapma.


# Mutlak degeri en buyuk uc kalintinin tarihleri.


# En buyuk kalintinin gunu: gozlem, trend, mevsim, kalinti.


# Kalintinin haftanin gunune gore ortalamasi: mutlak en buyuk.


# Trendin aya gore ortalamasi: en dusuk ve en yuksek ay.
