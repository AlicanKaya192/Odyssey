import pandas as pd


def month_table(dates, stores, amounts):
    df = pd.DataFrame({"date": dates, "store": stores, "amount": amounts})
    return {"months": [], "values": []}

DATES = ["2026-01-05", "2026-01-20", "2026-02-11", "2026-03-02"]
STORES = ["A", "B", "A", "B"]
result = month_table(DATES, STORES, [100, 50, 70, 30])
print(result["months"])
print(result["values"])
