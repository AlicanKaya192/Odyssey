import pandas as pd


def monthly_totals(dates, amounts):
    s = pd.Series(amounts, index=pd.to_datetime(dates))
    return {}

DATES = ["2026-01-05", "2026-01-20", "2026-03-02"]
print(*monthly_totals(DATES, [100, 50, 70]).items(), sep="\n")
