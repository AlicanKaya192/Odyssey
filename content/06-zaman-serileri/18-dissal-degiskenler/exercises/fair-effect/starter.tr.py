import numpy as np
import pandas as pd

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")


def effect(flag):
    # Her olay gununu, 7 gun onceki ve sonraki (olaysiz) gunlerle karsilastir.
    pass


# Kampanya ve tatil icin adil etki.


# Kaba etkiler: kampanya, tatil.
