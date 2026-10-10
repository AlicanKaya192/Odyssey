import pandas as pd


def store_share(stores, sales):
    df = pd.DataFrame({"store": stores, "sales": sales})
    totals = df.groupby("store")["sales"].transform("sum")
    return (df["sales"] / totals).round(3).tolist()

print(store_share(["A", "B", "A", "A"], [10.0, 5.0, 30.0, 60.0]))
