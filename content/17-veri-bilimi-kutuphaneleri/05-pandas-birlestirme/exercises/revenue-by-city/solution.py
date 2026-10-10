import pandas as pd


def revenue_by_city(orders, cities):
    left = pd.DataFrame(orders, columns=["order", "customer", "amount"])
    right = pd.DataFrame(cities, columns=["customer", "city"]).drop_duplicates("customer")
    joined = left.merge(right, on="customer", how="left", validate="many_to_one")
    return joined.groupby("city")["amount"].sum().to_dict()

ORDERS = [[1, 10, 250], [2, 20, 90], [3, 10, 40], [4, 40, 70]]
CITIES = [[10, "Izmir"], [10, "Ankara"], [20, "Bursa"], [40, "Izmir"]]
print(revenue_by_city(ORDERS, CITIES))
