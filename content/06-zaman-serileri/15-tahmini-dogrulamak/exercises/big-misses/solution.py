import numpy as np
import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

error = (visits - visits.shift(7)).dropna()


def scores(e):
    mae = float(e.abs().mean())
    rmse = float(np.sqrt((e ** 2).mean()))
    return mae, rmse


mae_all, rmse_all = scores(error)
print(round(mae_all, 1), round(rmse_all, 1), round(rmse_all / mae_all, 2))

worst = error.abs().sort_values(ascending=False).head(6).index.sort_values()
print(worst.strftime("%m-%d").tolist())

mae_rest, rmse_rest = scores(error.drop(worst))
print(round(mae_rest, 1), round(rmse_rest, 1), round(rmse_rest / mae_rest, 2))

print(round((1 - mae_rest / mae_all) * 100), round((1 - rmse_rest / rmse_all) * 100))
