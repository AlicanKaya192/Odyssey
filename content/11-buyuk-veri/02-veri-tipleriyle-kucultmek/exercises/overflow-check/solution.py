import pandas as pd

stock = pd.Series([90, 120, 250, 300, 40])

forced = stock.astype("int8")
print(forced.tolist())

broken = forced != stock
print(int(broken.sum()))
print(stock[broken].tolist())

safe = pd.to_numeric(stock, downcast="integer")
print(safe.dtype, safe.tolist())
