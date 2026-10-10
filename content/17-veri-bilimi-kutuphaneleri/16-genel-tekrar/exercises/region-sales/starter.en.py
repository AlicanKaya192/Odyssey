import pandas as pd


def region_sales(orders, regions):
    left = pd.DataFrame(orders, columns=["no", "city", "amount"])
    right = pd.DataFrame(regions, columns=["city", "region"])
    joined = left.merge(right, on="city")
    return {"sales": joined.groupby("region")["amount"].sum().to_dict(), "unmatched": []}

ORDERS = [[1, " izmir", 120], [2, "Izmir ", 80], [3, "ANKARA", 50], [4, "bursa", 70]]
REGIONS = [["Izmir", "Aegean"], ["Ankara", "Central"]]
result = region_sales(ORDERS, REGIONS)
print(result["sales"])
print(result["unmatched"])
