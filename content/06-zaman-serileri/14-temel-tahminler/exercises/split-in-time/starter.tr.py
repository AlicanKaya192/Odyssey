import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

# Son 28 gun test, oncesi egitim.


# Uzunluklar.


# Egitimin son tarihi, testin ilk tarihi.


# Ufuk ve gelecek tarihlerin indeksi.


# Indeksin ilk ve son tarihi.


# Indeks testin indeksiyle ayni mi?


# Egitim ve test ortalamasi.
