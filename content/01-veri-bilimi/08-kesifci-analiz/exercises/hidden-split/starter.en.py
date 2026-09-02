import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir",
             "Ankara", "Bursa", "Izmir", "Ankara", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27, 33, 29],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11, 6, 13],
    "score": [88, 62, 82, 45, 91, 70, 51, 84, 66, 89],
})

records = pd.DataFrame({
    "team": ["A"] * 10 + ["B"] * 10,
    "level": ["easy"] * 8 + ["hard"] * 2 + ["easy"] * 2 + ["hard"] * 8,
    "score": [80, 80, 80, 80, 80, 80, 80, 80, 50, 50,
              85, 85, 55, 55, 55, 55, 55, 55, 55, 55],
})

# Compute the team averages and print A and B side by side.


# Print the team with the higher average.


# Print how many hard questions each team answered, side by side.


# Print the averages on the easy questions, side by side.


# Print the averages on the hard questions, side by side.
