import pandas as pd


def store_share(stores, sales):
    df = pd.DataFrame({"store": stores, "sales": sales})
    return (df["sales"] / df["sales"].sum()).round(3).tolist()

print(store_share(["A", "B", "A", "A"], [10.0, 5.0, 30.0, 60.0]))
