import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
day = pd.Timestamp("2024-03-09")

# Uc gun adi: day, 365 gun once, 364 gun once.


# Yillik buyume (%): shift(365) ile ve shift(364) ile.


# O gunun iki buyume orani (bir ondalik).


# 2024'un butun gunlerinde iki oranin standart sapmasi (bir ondalik).
