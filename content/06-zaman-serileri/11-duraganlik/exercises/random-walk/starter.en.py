import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()

# Correlation of the level and of the change with one day earlier.


# The naive forecast and the 20-day mean forecast: mean absolute error.


# Share of up days; the same share on days after an up day.
