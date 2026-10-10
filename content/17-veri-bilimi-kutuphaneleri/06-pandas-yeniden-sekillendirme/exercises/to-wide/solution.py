import pandas as pd


def to_wide(records, months):
    long = pd.DataFrame(records, columns=["city", "month", "sales"])
    wide = long.pivot(index="city", columns="month", values="sales")[months]
    return {"columns": wide.columns.tolist(), "values": wide.values.tolist()}

RECORDS = [["Izmir", "jan", 80], ["Ankara", "jan", 120], ["Izmir", "feb", 95],
           ["Ankara", "feb", 110], ["Izmir", "mar", 70], ["Ankara", "mar", 90]]
result = to_wide(RECORDS, ["jan", "feb", "mar"])
print(result["columns"])
print(*result["values"], sep="\n")
