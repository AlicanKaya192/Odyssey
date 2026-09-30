import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

year = s.loc["2024"]
ma7 = s.rolling(7).mean().loc["2024"]
ma28 = s.rolling(28).mean().loc["2024"]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(year.index, year.values, color="lightgray", linewidth=0.8, label="daily")
ax.plot(ma7.index, ma7.values, linewidth=2, label="7-day mean")
ax.plot(ma28.index, ma28.values, linewidth=2, label="28-day mean")
ax.legend()
fig.savefig("chart.png")

print(len(ax.lines))
print([t.get_text() for t in ax.get_legend().get_texts()])
print(int(ma7.isna().sum()), int(ma28.isna().sum()))
