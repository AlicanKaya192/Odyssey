import numpy as np
import pandas as pd

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def backtest(forecast):
    # Her kesimde 28 gunluk MAE; ortalama ve en kotu.
    pass


def naive(train, index):
    pass


def seasonal_naive(train, index):
    pass


def week_mean(train, index):
    pass


# Uc taban cizginin sonucu.


# Test donemindeki ortalama ve mevsimsel naif MAE'sinin yuzde orani.
