import pandas as pd

raw = pd.read_csv("sales_messy.csv", parse_dates=["date"])
full = raw.groupby("date")["sales"].sum().sort_index().asfreq("D")
truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Eksik gunlerin indeksi.


def score(filled):
    # Eksik gunlerde ortalama mutlak hata (bir ondalik).
    pass


# Dort yontem: ffill, linear, week ago, both sides.


# Her biri icin: ad ve hata.


# 10 Subat: gercek ve dort yontemin degeri.
