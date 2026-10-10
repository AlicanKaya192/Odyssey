import pandas as pd


def order_totals(prices, qtys):
    df = pd.DataFrame({"price": prices, "qty": qtys})
    result = []
    for _, row in df.iterrows():
        result.append(round(row["price"] * row["qty"], 2))
    return result

print(order_totals([10.0, 8.5, 3.2], [2, 3, 10]))
