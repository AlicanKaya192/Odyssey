import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

ytd_2023 = s.loc["2023"].cumsum()
ytd_2024 = s.loc["2024"].cumsum()

print((ytd_2023 >= 50000).idxmax().strftime("%Y-%m-%d"))
print((ytd_2024 >= 50000).idxmax().strftime("%Y-%m-%d"))

half_2023 = ytd_2023.loc["2023-06-30"]
half_2024 = ytd_2024.loc["2024-06-30"]
print(half_2023, half_2024)
print(round(float((half_2024 / half_2023 - 1) * 100), 1))
