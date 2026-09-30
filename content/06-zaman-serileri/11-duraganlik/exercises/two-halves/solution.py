import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def halves(x):
    half = len(x) // 2
    first, second = x.iloc[:half], x.iloc[half:]
    return (round(float(first.mean()), 2), round(float(second.mean()), 2),
            round(float(first.std()), 2), round(float(second.std()), 2))


print(halves(k))

change = k.diff().dropna()
print(halves(change))
