import pandas as pd
from pandas.tseries.offsets import BDay, CustomBusinessDay

orders = ["2024-03-08", "2024-04-09", "2024-06-14"]

# Read the holiday dates.


# A business-day offset that knows the holidays.


# Working days in 2024: without and with holidays.


# Each order: the delivery day with BDay(3) and with 3 * workday.
