import numpy as np
import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")


def effect(flag):
    differences = []
    for day in c.index[c[flag] == 1]:
        values = []
        for neighbour in (day - pd.Timedelta(days=7), day + pd.Timedelta(days=7)):
            if neighbour not in c.index:
                continue
            row = c.loc[neighbour]
            if row["promo"] == 0 and row["holiday"] == 0:
                values.append(row["sales"])
        if values:
            differences.append(c.loc[day, "sales"] - np.mean(values))
    return round(float(np.mean(differences)), 1), len(differences)


print(effect("promo"))
print(effect("holiday"))


def rough(flag):
    on = c.loc[c[flag] == 1, "sales"].mean()
    off = c.loc[c[flag] == 0, "sales"].mean()
    return round(float(on - off), 1)


print(rough("promo"), rough("holiday"))
