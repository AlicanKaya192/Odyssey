import pandas as pd
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Elle: 1..7 gecikme icin s.corr(s.shift(k)) (iki ondalik, liste).


# acf ile: gecikme 0 haric (iki ondalik, liste).


# En yuksek degerin gecikmesi.


# acf dizisinin uzunlugu ve ilk elemani.
