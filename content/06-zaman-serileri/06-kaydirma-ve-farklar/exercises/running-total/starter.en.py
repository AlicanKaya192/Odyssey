import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Running totals for 2023 and 2024.


# The date each year first reached 50000.


# Running totals on 30 June (2023, 2024).


# First half of 2024 against first half of 2023, percent higher (one decimal).
