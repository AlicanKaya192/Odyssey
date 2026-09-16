import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("exam.csv")
mean = data["score"].mean()
median = data["score"].median()

print(round(mean, 2))
print(median)
print(round(data["score"].std(), 2))
print(mean < median)

fig, ax = plt.subplots()
ax.hist(data["score"], bins=6)
ax.axvline(mean, color="red", linestyle="--", label="mean")
ax.axvline(median, color="green", label="median")
ax.set_title("Exam scores")
ax.set_xlabel("Score")
ax.legend()
fig.savefig("histogram.png")
