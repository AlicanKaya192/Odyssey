import numpy as np
import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")


def effect(flag):
    # Compare each event day with the (event-free) days 7 days before and after.
    pass


# The fair effect for campaign and holiday.


# The rough effects: campaign, holiday.
