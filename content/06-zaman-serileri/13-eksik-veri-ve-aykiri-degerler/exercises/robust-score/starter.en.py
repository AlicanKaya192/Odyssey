import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

# Mean, median, standard deviation.


# The z-score; days with |z| > 3.


def robust(x):
    # A robust score based on the median and the MAD.
    pass


# The MAD.


# The 5 days with the largest robust score, and their scores.


# 8 October: z-score and robust score.
