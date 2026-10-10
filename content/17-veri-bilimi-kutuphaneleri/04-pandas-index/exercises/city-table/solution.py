import pandas as pd


def city_table(rows):
    df = pd.DataFrame(rows, columns=["city", "year", "sales"])
    table = df.groupby(["city", "year"])["sales"].sum().unstack(fill_value=0)
    return {"years": table.columns.tolist(), "cities": table.index.tolist(),
            "values": table.values.tolist()}

ROWS = [["Izmir", 2024, 30], ["Izmir", 2024, 50], ["Ankara", 2025, 110],
        ["Ankara", 2024, 120], ["Bursa", 2024, 50], ["Izmir", 2025, 95]]
result = city_table(ROWS)
print(result["years"])
print(result["cities"])
print(*result["values"], sep="\n")
