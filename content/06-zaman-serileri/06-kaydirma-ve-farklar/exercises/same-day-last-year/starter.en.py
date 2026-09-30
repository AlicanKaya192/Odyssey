import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
day = pd.Timestamp("2024-03-09")

# Three day names: day, 365 days earlier, 364 days earlier.


# Yearly growth (%): with shift(365) and with shift(364).


# That day's two growth rates (one decimal).


# Standard deviation of the two rates over every day of 2024 (one decimal).
