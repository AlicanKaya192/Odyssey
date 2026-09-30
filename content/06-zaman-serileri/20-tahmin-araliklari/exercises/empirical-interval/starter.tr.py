import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Bir gun sonrasi hatasi; 2023 (past) ve 2024 (future).


# past'in %10 ve %90 yuzdelikleri.


# 15 Mart 2024: tahmin, alt uc, ust uc, gercek.


def coverage(level):
    # past'tan iki yuzdelik; future hatalarinin aralikta kalma orani.
    pass


# Kapsama: 0.5, 0.8, 0.95.
