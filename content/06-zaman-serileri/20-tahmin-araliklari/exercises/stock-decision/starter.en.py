import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)
past = error.loc["2023"]
base = s.shift(7).loc["2024"]
actual = s.loc["2024"]


def cost(order):
    # Days out of stock, total short, total over, total cost.
    pass


# q = 0.5, 0.8, 0.9, 0.95: q and the result of cost.


# The quantile the formula says.


# The q with the lowest cost and the saving over the point forecast.
