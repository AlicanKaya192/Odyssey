import numpy as np
import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

# Gunluk degisimin standart sapmasi.


# Son degerden h = 1, 10, 40 icin %95 aralik.


def coverage(h, widen):
    # Butun gunlerden h gun sonraki hata; sinirin icinde kalma orani.
    pass


# h = 1, 10, 40: karekok kuraliyla ve sabit genislikle kapsama.
