import pandas as pd


def month_table(dates, stores, amounts):
    df = pd.DataFrame({"date": dates, "store": stores, "amount": amounts})
    df["month"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.to_period("M").astype(str)
    table = df.pivot_table(index="month", columns="store", values="amount", aggfunc="sum", fill_value=0)
    return {"months": table.index.tolist(), "values": table.values.tolist()}

DATES = ["2026-01-05", "2026-01-20", "2026-02-11", "2026-03-02"]
STORES = ["A", "B", "A", "B"]
result = month_table(DATES, STORES, [100, 50, 70, 30])
print(result["months"])
print(result["values"])
