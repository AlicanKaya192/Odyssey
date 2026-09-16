import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("students.csv")
averages = data.groupby("city")["score"].mean()

fig, ax = plt.subplots()
ax.bar(averages.index, averages.values)
ax.set_title("Average score by city")
ax.set_ylim(68, 90)
fig.savefig("misleading.png")
print(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]))

ax.set_ylim(0, 100)
fig.savefig("honest.png")
print(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]))

print(round(averages.max() / averages.min(), 2))
