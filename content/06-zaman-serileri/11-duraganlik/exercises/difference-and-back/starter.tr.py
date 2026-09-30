import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Standart sapma: seri, diff(), diff(7).


# NaN sayilari: seri, diff(), diff(7).


# Haftanin gunune gore ortalama: en yuksek - en dusuk (diff, diff(7)).


# Duz farki geri cevir ve karsilastir.


# Mevsimsel farki bir adim geri cevir: hesaplanan ve gercek son deger.
