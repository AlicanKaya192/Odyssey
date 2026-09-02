import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila", "Kaan", "Ela"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir", "Bursa", "Izmir"],
    "grade": ["A", "B", "A", "C", "B", "A", "B", "C"],
    "score": [82, 74, 91, 68, 88, 76, 70, 64],
})

# Group by city and grade, compute the mean and round to one place.
# Keep the result in a Series called result.


# Print result.


# Flatten result and print its shape.
