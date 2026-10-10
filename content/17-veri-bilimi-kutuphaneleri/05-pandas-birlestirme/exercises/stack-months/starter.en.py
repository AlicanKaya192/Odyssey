import pandas as pd


def stack_months(months):
    frames = [pd.DataFrame(rows, columns=["city", "sales"]) for rows in months.values()]
    return {"rows": 0, "index": [], "totals": {}}

MONTHS = {"jan": [["Izmir", 80], ["Ankara", 120]], "feb": [["Bursa", 50]],
          "mar": [["Izmir", 95], ["Bursa", 65], ["Van", 10]]}
result = stack_months(MONTHS)
print(result["rows"], result["index"])
print(result["totals"])
