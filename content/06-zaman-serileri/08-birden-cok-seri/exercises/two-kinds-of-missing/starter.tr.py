import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

# C'nin NaN oldugu gunlerin gun adlari (farkli olanlar, liste).


# C: NaN atlanarak ve fillna(0) ile ortalama (bir ondalik).


# D: ayni iki ortalama.


# Dort magazanin gunluk toplami: 30 Nisan ve 1 Mayis.


# A + B + C toplami: ayni iki gun.
