import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

# Aylik ortalamalar.


# Mayis = 100 endeksi.


# Aralik endeks degerleri (sozluk, bir ondalik).


# Ceyreklik paylar (%); son ceyregin paylari (sozluk).


# A'nin payi: son ceyrek - ilk ceyrek (puan, bir ondalik).
