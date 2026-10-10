import pandas as pd


def city_table(rows):
    df = pd.DataFrame(rows, columns=["city", "year", "sales"])
    return {"years": [], "cities": [], "values": []}

ROWS = [["Izmir", 2024, 30], ["Izmir", 2024, 50], ["Ankara", 2025, 110],
        ["Ankara", 2024, 120], ["Bursa", 2024, 50], ["Izmir", 2025, 95]]
result = city_table(ROWS)
print(result["years"])
print(result["cities"])
print(*result["values"], sep="\n")
