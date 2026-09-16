import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("sales.csv")

fig, ax = plt.subplots()
ax.plot(data["month"], data["sales"], marker="o")
ax.set_title("Monthly sales")
ax.set_ylabel("Sales (thousands)")
fig.savefig("chart.png")

print(len(ax.lines))
print(data.loc[data["sales"].idxmax(), "month"])
print(int(data["sales"].iloc[-1] - data["sales"].iloc[0]))
print(ax.get_ylabel())
