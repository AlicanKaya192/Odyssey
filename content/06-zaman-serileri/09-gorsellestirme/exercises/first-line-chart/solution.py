import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s.index, s.values, linewidth=0.8)
ax.set_title("Daily sales")
ax.set_ylabel("Units")
fig.savefig("chart.png")

print(len(ax.lines))
print(ax.get_title())
print(ax.get_ylabel())
width, height = fig.get_size_inches()
print(float(width), float(height))
