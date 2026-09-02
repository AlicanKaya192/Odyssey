import pandas as pd

raw = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 5, 6],
    "city": ["Ankara", "Izmir ", "ankara", "Bursa", "Izmir", "Izmir", "ANKARA"],
    "score": ["82", "74", "91", None, "68", "68", "abc"],
})

# Take a copy of the raw data.


# Clean the city column and convert it to title case.


# Convert the score column to numbers, unconvertible values to blank.


# Keep the starting row count in a variable.


# Drop duplicates by id and keep the remaining row count.


# Count how many records are left with a blank score.


# Drop the rows with a blank score.


# Print the four numbers side by side on one line.


# Print the count and mean by city.
