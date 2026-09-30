import numpy as np
import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

# One-step seasonal naive error.


# MAE, RMSE, RMSE / MAE.


# The 6 days with the largest absolute error (in date order, "%m-%d").


# With those 6 days removed: MAE, RMSE, ratio.


# By what percentage did the MAE and the RMSE fall?
