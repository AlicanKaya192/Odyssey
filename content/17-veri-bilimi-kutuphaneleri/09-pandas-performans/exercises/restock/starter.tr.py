import pandas as pd


def restock(cities, stock, amount):
    df = pd.DataFrame({"city": cities, "stock": stock})
    df[df["stock"] == 0]["stock"] = amount
    return df["stock"].tolist()

print(restock(["Izmir", "Ankara", "Bursa"], [5, 0, 0], 10))
