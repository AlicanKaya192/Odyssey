import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("students.csv")
averages = data.groupby("city")["score"].mean()

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))

left.bar(averages.index, averages.values)
left.set_ylim(0, 100)
left.set_title("Average score")

right.scatter(data["hours"], data["score"])
right.set_title("Hours vs score")
right.set_xlabel("Hours")
right.set_ylabel("Score")

fig.tight_layout()
fig.savefig("panels.png")

print(len(fig.axes))
print(left.get_title(), "|", right.get_title())
print(round(data["hours"].corr(data["score"]), 2))
