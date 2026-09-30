import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def halves(x):
    # Split the series in two; return the two means and the two std values.
    pass


# For the price.


# For the daily change.
