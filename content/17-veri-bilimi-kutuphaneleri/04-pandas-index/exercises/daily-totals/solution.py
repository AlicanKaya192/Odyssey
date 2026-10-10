import pandas as pd


def daily_totals(days, amounts):
    s = pd.Series(amounts, index=days)
    return s.groupby(level=0).sum().to_dict()

print(daily_totals(["mon", "tue", "mon", "wed", "tue"], [10, 20, 30, 5, 1]))
