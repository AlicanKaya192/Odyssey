import pandas as pd


def daily_change(values):
    s = pd.Series(values)
    return s.diff().dropna().round(3).tolist()

print(daily_change([100, 110, 99, 120, 120]))
