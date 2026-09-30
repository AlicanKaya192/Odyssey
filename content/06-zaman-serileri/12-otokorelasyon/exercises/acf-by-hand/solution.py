import pandas as pd
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

by_hand = [round(float(s.corr(s.shift(k))), 2) for k in range(1, 8)]
print(by_hand)

values = acf(s, nlags=7)
print([round(float(v), 2) for v in values[1:]])

print(int(values[1:].argmax()) + 1)
print(len(values), float(values[0]))
