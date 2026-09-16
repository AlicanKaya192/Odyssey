import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("students.csv")

fig, ax = plt.subplots()
counts, edges, bars = ax.hist(data["score"], bins=5)
ax.set_title("Score distribution")
ax.set_xlabel("Score")
ax.set_ylabel("Students")
fig.savefig("histogram.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print(len(bars))
print([int(c) for c in counts])
print(round(data["score"].mean(), 1), data["score"].median())
print(ax.get_title())
