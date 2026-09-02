import pandas as pd

raw = pd.DataFrame({
    "Name ": [" Ada", "Kerem", "Mina ", "Deniz", "Efe", "Sila"],
    "City ": ["ankara", "Izmir ", "ANKARA", " bursa", "izmir", "Ankara "],
    "score": ["82", "74", "91", "68", "88", "76"],
})

# Take a copy so the raw data stays intact.


# Strip the column names and lower-case them.


# Strip the spaces in the name column.


# Clean the city column and convert it to title case.


# Convert the score column to numbers.


# Print the column names, the types, the city counts (dict) and the mean.
