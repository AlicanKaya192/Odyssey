import numpy as np
import pandas as pd

table = pd.read_csv("store_sales.csv")
values = table["sales"].to_numpy()

lag1 = np.corrcoef(values[:-1], values[1:])[0, 1]
lag7 = np.corrcoef(values[:-7], values[7:])[0, 1]

mixed = table.sample(frac=1, random_state=42)["sales"].to_numpy()
shuffled = np.corrcoef(mixed[:-1], mixed[1:])[0, 1]

print(round(float(lag1), 3))
print(round(float(lag7), 3))
print(round(float(shuffled), 3))
