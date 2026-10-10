import pandas as pd


def sales_in_year(rows, year):
    df = pd.DataFrame(rows, columns=["city", "year", "sales"])
    m = df.set_index(["city", "year"]).sort_index()
    return m.xs(year, level="year")["sales"].to_dict()

ROWS = [["Izmir", 2024, 80], ["Izmir", 2025, 95], ["Ankara", 2024, 120],
        ["Ankara", 2025, 110], ["Bursa", 2024, 50], ["Bursa", 2025, 65]]
print(sales_in_year(ROWS, 2025))
