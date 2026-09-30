import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last_week = train.iloc[-7:].to_numpy()
    return [last_week[i % 7] for i in range(h)]


def evaluate(cut):
    # Training up to cut, the next 28 days the test; MAE, bias, days too low.
    pass


# Two experiments: 5 November and 3 December.


# The 3 December experiment: mean of the error by week (a list).
