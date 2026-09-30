import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

# Carpimsal ayristirma, period=12.


# Arindirilmis seri.


# Haziran-Eylul 2024: ham degerler (liste).


# Ayni aylar: arindirilmis degerler (bir ondalik, liste).


# Eylul 2024 yuzde degisimi: ham ve arindirilmis.


# Aylik yuzde degisimin standart sapmasi: ham ve arindirilmis.
