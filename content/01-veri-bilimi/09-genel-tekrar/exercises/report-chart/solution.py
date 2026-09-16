import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("students.csv")
averages = data.groupby("city")["score"].mean().round(1).sort_values(ascending=False)
print(averages.to_dict())

fig, ax = plt.subplots()
ax.bar(averages.index, averages.values)
ax.set_ylim(0, 100)
ax.set_title("Average score by city")
ax.set_ylabel("Score")
fig.savefig("report.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print(len(ax.patches), int(ax.get_ylim()[1]), ax.get_title())
