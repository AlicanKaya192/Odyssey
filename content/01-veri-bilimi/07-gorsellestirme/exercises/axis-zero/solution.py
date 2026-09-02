import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

fig, ax = plt.subplots()
ax.bar(data["city"], data["score"])

low, high = ax.get_ylim()
print(int(low) == 0)

ax.set_ylim(0, 100)
low, high = ax.get_ylim()
print(int(low), int(high))
