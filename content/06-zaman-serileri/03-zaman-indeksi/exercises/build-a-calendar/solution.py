import pandas as pd

business = pd.date_range("2024-03-01", "2024-03-31", freq="B")
print(len(business))

month_ends = pd.date_range("2024-01-01", "2024-06-30", freq="ME")
print(month_ends.strftime("%m-%d").tolist())

shifts = pd.date_range("2024-03-09 06:00", periods=4, freq="8h")
print(shifts.strftime("%d %H:%M").tolist())

mondays = pd.date_range("2024-03-01", "2024-03-31", freq="W-MON")
print(len(mondays), mondays[0].strftime("%Y-%m-%d"))
