import numpy as np
import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]
periods = [("2013", "2016"), ("2017", "2020"), ("2021", "2024")]

# Duz farkin uc donemdeki standart sapmasi (bir ondalik, liste).


# Log farkin uc donemdeki standart sapmasi (uc ondalik, liste).


# Son donem / ilk donem orani: duz fark, log fark.


# Yillik buyume orani (yuzde, bir ondalik).


# growth'un ilk dolu tarihi ve NaN sayisi.
