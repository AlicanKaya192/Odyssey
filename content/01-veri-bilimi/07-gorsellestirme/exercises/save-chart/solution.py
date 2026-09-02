import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

from pathlib import Path

fig, ax = plt.subplots()
ax.hist(data["score"], bins=4)
ax.set_title("Score distribution")
ax.set_xlabel("Score")

fig.savefig("chart.png", dpi=150, bbox_inches="tight")
plt.close(fig)

path = Path("chart.png")
print(path.exists())
print(path.stat().st_size > 0)
print(ax.get_title())
