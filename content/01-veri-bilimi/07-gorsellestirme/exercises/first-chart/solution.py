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
ax.set_title("Average score by city")
ax.set_xlabel("City")
ax.set_ylabel("Score")

print(len(ax.patches))
print(ax.get_title())
print(ax.get_xlabel())
print(ax.get_ylabel())
