import numpy as np
import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
v = v.astype(float)


def best_split(x, margin=14):
    # En kucuk kare toplamini veren k ve kazanc.
    pass


# Ham seri: degisim gunu ve kazanc.


# Hafta sonu etkisini gider: ratio, adjusted; degisim gunu ve kazanc.


# Uc anomaliyi onar (clean): gun, kazanc, once, sonra, yuzde degisim.


# clean'in iki parcasinda ikinci kesimin kazanci.
