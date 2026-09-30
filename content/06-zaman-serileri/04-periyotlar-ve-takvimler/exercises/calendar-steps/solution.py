import pandas as pd
from pandas.tseries.offsets import MonthEnd

starts = ["2024-01-31", "2024-02-29", "2024-03-31", "2024-08-30"]

for text in starts:
    start = pd.Timestamp(text)
    by_days = start + pd.Timedelta(days=30)
    by_month = start + pd.DateOffset(months=1)
    print(text, by_days.strftime("%Y-%m-%d"), by_month.strftime("%Y-%m-%d"))

day = pd.Timestamp("2024-03-09")
month_end = day + MonthEnd(0)
print(month_end.strftime("%Y-%m-%d"))
print((month_end - day).days)
