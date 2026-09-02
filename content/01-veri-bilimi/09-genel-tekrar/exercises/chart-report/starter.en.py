import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir", "Ankara"],
    "score": [88, 62, 82, 45, 91, 70],
})

# Compute the average score by city, round to one decimal
# and print it as a dict.


# Create a canvas and a drawing area.


# Draw the averages as a bar chart.


# Force the axis to run from 0 to 100.


# Set the title and the y axis label.


# Save it as report.png and close the canvas.


# Print the bar count, the upper bound, the title and whether the file exists.
