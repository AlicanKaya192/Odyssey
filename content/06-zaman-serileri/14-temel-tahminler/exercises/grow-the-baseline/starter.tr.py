import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# base: 2023'un on iki degeri.


# Kayma: her aya slope * 12 ekle.


# Buyume: orani yazdir, her ayi oranla carp.


# Uc tahmin: ad, MAE, yuzde hata.


# Buyumeli tahminin mevsimsel naife gore becerisi.


# Agustos 2024: gercek ve uc tahmin.
