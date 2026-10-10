import pandas as pd


def cities_for(rows, codes):
    df = pd.DataFrame(rows, columns=["code", "city", "stock"])
    part = df.head(len(codes))
    return [part["city"].tolist(), int(part["stock"].sum())]

STOCK = [["A7", "Izmir", 14], ["B2", "Ankara", 3], ["C9", "Bursa", 8]]
print(cities_for(STOCK, ["C9", "A7"]))
