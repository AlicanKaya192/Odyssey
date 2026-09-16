import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("students.csv")
averages = data.groupby("city")["score"].mean()

fig, ax = plt.subplots()
ax.bar(averages.index, averages.values)
ax.set_title("Average score by city")
ax.set_xlabel("City")
ax.set_ylabel("Score")
fig.savefig("chart.png")

print(len(ax.patches))
print(ax.get_title())
print(ax.get_xlabel(), "|", ax.get_ylabel())
