import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

months = ["Jan", "Feb", "Mar", "Apr"]
sales = [120, 150, 130, 180]

fig, ax = plt.subplots()
ax.plot(months, sales, marker="o")
ax.set_title("Monthly sales")
ax.set_ylabel("Sales (thousands)")

print(len(ax.lines))
print(ax.lines[0].get_ydata().tolist())
print(ax.get_ylabel())
