import pandas as pd


def order_totals(prices, qtys):
    df = pd.DataFrame({"price": prices, "qty": qtys})
    return (df["price"] * df["qty"]).round(2).tolist()

print(order_totals([10.0, 8.5, 3.2], [2, 3, 10]))
