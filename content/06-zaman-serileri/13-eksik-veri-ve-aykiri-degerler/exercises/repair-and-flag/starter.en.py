import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]
days = pd.to_datetime(["2024-03-14", "2024-06-20", "2024-10-08"])

# Take a copy, set the three days to NaN.


# Fill with the average of a week before and a week after.


# The new values of the three days (a list).


# The table: visits, clean, repaired; number of rows and total of repaired.


# Standard deviation: before, after.


# Thursday mean: before, after.


# Total effect of the two campaign days.
