import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

# Draw a histogram of the score column (bins=4).


# Set the title and the x axis label.


# Save the chart as chart.png (dpi=150, bbox_inches="tight").


# Close the canvas.


# Print whether the file exists, whether its size is over zero, and the title.
