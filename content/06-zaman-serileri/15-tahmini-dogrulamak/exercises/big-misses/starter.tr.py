import numpy as np
import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

# Tek adimli mevsimsel naif hatasi.


# MAE, RMSE, RMSE / MAE.


# Mutlak hatasi en buyuk 6 gun (tarih sirasiyla, "%m-%d").


# O 6 gun cikarilinca: MAE, RMSE, oran.


# MAE ve RMSE yuzde kac dustu?
