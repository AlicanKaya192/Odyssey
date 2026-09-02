import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir",
             "Ankara", "Bursa", "Izmir", "Ankara", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27, 33, 29],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11, 6, 13],
    "score": [88, 62, 82, 45, 91, 70, 51, 84, 66, 89],
})

values = pd.Series([48, 52, 50, 51, 49, 53, 50, 140])

# Compute the first and third quartiles and print them side by side.


# Compute the lower and upper bounds and print them side by side.


# Print the values outside those bounds as a list.


# Print the mean (two decimals) and the median side by side.
