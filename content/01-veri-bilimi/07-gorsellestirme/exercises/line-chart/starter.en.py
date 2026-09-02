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

# Draw a line chart with months on x and sales on y.
# Mark the points with marker="o".


# Set the title and the y axis label.


# Print the number of lines, the line's y data and the y label.
