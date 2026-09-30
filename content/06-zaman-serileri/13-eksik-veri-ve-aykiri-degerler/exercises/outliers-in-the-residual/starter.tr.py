import pandas as pd
from statsmodels.tsa.seasonal import STL

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]


def robust(x):
    median = x.median()
    mad = (x - median).abs().median()
    return 0.6745 * (x - median) / mad


# Ham seride ceyrekler arasi aralik kurali: isaretlenen gun sayisi.


# Bunlardan 2 Eylul'den sonra olanlarin sayisi.


# Dayanikli STL, kalintinin dayanikli puani.


# Puani en buyuk 5 gun ve puanlari.


# |puan| > 3.5 ve |puan| > 20 olan gun sayilari.
