import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

# Create a canvas with two drawing areas side by side, figsize=(10, 4).


# On the left draw the city-score bars, set the axis to 0-100, title Scores.


# On the right draw an hours-score scatter plot with a title and x label.


# Tighten the layout.


# Print the area count, the bar count, both titles and the left upper bound.
