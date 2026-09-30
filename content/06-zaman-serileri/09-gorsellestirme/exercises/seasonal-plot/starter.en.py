import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# The month x year table of means.


# Shape and columns.


# One line per year, legend, save.


# Each year's lowest and highest month.


# Mean of the 2024 - 2022 differences (one decimal).
