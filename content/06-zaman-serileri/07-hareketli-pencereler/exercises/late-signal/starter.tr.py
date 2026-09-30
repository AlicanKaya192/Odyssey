import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Geriye donuk ve ortalanmis 28 gunluk ortalama.


# 2023-11-15 .. 2024-02-15 araliginda tepe tarihleri (once ortalanmis).


# Iki tarih arasindaki gun farki.


# Iki tepenin degeri (bir ondalik).


# Son 14 gundeki NaN sayilari (once ortalanmis).
