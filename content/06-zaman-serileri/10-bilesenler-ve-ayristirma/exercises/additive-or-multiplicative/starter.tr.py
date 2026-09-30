import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

# Iki model: additive ve multiplicative, period=12.


# Toplamsal kalintinin mutlak degeri, yila gore ortalama: 2013, 2019, 2023.


# Toplamsal kalinti: Temmuz 2013 ve Temmuz 2023.


# Carpimsal kalinti yuzde sapma olarak; ayni uc yilin ortalamasi.


# Yuzde sapmanin en buyugu.


# En kucuk ve en buyuk mevsim carpani: ay ve carpan.
