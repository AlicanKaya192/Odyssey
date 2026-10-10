import pandas as pd


def cities_for(rows, codes):
    items = pd.DataFrame(rows, columns=["code", "city", "stock"]).set_index("code")
    part = items.loc[codes]
    return [part["city"].tolist(), int(part["stock"].sum())]

STOCK = [["A7", "Izmir", 14], ["B2", "Ankara", 3], ["C9", "Bursa", 8]]
print(cities_for(STOCK, ["C9", "A7"]))
