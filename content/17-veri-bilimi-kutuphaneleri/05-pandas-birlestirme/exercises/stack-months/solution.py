import pandas as pd


def stack_months(months):
    frames = [pd.DataFrame(rows, columns=["city", "sales"]) for rows in months.values()]
    stacked = pd.concat(frames, keys=list(months))
    flat = pd.concat(frames, ignore_index=True)
    totals = stacked.groupby(level=0, sort=False)["sales"].sum()
    return {"rows": len(stacked), "index": flat.index.tolist(), "totals": totals.to_dict()}

MONTHS = {"jan": [["Izmir", 80], ["Ankara", 120]], "feb": [["Bursa", 50]],
          "mar": [["Izmir", 95], ["Bursa", 65], ["Van", 10]]}
result = stack_months(MONTHS)
print(result["rows"], result["index"])
print(result["totals"])
