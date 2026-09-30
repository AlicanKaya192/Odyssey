import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# 2023 ve 2024 icin birikimli toplam.


# Her yilin 50000'e ilk ulastigi tarih.


# 30 Haziran'daki birikimli toplamlar (2023, 2024).


# 2024 ilk yarisi, 2023 ilk yarisina gore yuzde kac yuksek (bir ondalik).
