import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir", "Ankara"],
    "score": [88, 62, 82, 45, 91, 70],
})

averages = data.groupby("city")["score"].mean().round(1)
print(averages.to_dict())

fig, ax = plt.subplots()
ax.bar(averages.index, averages.values)
ax.set_ylim(0, 100)
ax.set_title("Average score by city")
ax.set_ylabel("Score")

fig.savefig("report.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print(len(ax.patches), int(ax.get_ylim()[1]), ax.get_title(),
      Path("report.png").exists())
