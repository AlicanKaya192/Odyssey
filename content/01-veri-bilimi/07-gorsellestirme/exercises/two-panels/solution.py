import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))

left.bar(data["city"], data["score"])
left.set_ylim(0, 100)
left.set_title("Scores")

right.scatter(data["hours"], data["score"])
right.set_title("Hours vs score")
right.set_xlabel("Hours")

fig.tight_layout()

print(len(fig.axes))
print(len(left.patches))
print(left.get_title(), "|", right.get_title())
print(int(left.get_ylim()[1]))
