import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from orders_data import make_orders


def category_quantity(path):
    part = pd.read_parquet(path)
    return part.groupby("category")["quantity"].sum()


if __name__ == "__main__":
    orders = make_orders(100_000)
    paths = []
    for i in range(4):
        path = f"part-{i}.parquet"
        orders.iloc[i * 25_000:(i + 1) * 25_000].to_parquet(path, index=False)
        paths.append(path)

    with ProcessPoolExecutor(max_workers=2) as ex:
        combined = pd.concat(ex.map(category_quantity, paths)).groupby(level=0).sum()

    combined = combined.sort_index()
    for category, quantity in combined.items():
        print(category, quantity)

    whole = orders.groupby("category")["quantity"].sum().sort_index()
    print(combined.equals(whole))
