import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

table = s.groupby([s.index.month, s.index.year]).mean().unstack()
print(table.shape)
print(table.columns.tolist())

fig, ax = plt.subplots(figsize=(8, 4))
for year in table.columns:
    ax.plot(table.index, table[year], marker="o", label=str(year))
ax.set_xticks(range(1, 13))
ax.legend()
fig.savefig("chart.png")

for year in table.columns:
    print(year, table[year].idxmin(), table[year].idxmax())

print(round(float((table[2024] - table[2022]).mean()), 1))
