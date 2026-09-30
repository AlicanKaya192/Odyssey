import pandas as pd
from pandas.tseries.offsets import BDay, CustomBusinessDay

orders = ["2024-03-08", "2024-04-09", "2024-06-14"]

holidays = pd.read_csv("holidays_2024.csv", parse_dates=["date"])["date"]
workday = CustomBusinessDay(holidays=holidays)

plain = pd.bdate_range("2024-01-01", "2024-12-31")
real = pd.date_range("2024-01-01", "2024-12-31", freq=workday)
print(len(plain), len(real))

for text in orders:
    order = pd.Timestamp(text)
    without = order + BDay(3)
    with_holidays = order + 3 * workday
    print(text, without.strftime("%Y-%m-%d"), with_holidays.strftime("%Y-%m-%d"))
