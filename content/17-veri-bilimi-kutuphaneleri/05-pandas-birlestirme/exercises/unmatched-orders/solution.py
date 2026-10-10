import pandas as pd


def unmatched_orders(orders, customers):
    left = pd.DataFrame(orders, columns=["order", "customer", "amount"])
    right = pd.DataFrame(customers, columns=["customer", "name"])
    check = left.merge(right, on="customer", how="outer", indicator=True)
    lost = check.loc[check["_merge"] == "left_only", "order"]
    return lost.astype(int).tolist()

ORDERS = [[1, 10, 250], [2, 20, 90], [3, 10, 40], [4, 40, 70]]
CUSTOMERS = [[10, "Ada"], [20, "Can"], [30, "Eda"]]
print(unmatched_orders(ORDERS, CUSTOMERS))
