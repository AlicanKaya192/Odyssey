import pandas as pd


def attach_names(orders, customers):
    left = pd.DataFrame(orders, columns=["order", "customer", "amount"])
    right = pd.DataFrame(customers, columns=["customer", "name"])
    joined = left.merge(right, on="customer")
    return joined["name"].tolist()

ORDERS = [[1, 10, 250], [2, 20, 90], [3, 10, 40], [4, 40, 70]]
CUSTOMERS = [[10, "Ada"], [20, "Can"], [30, "Eda"]]
print(attach_names(ORDERS, CUSTOMERS))
