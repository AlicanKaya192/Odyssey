import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def fitted_median(rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), ["size"])]).fit(df)
    return float(prep.named_transformers_["num"].statistics_[0])

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
print(fitted_median(ROWS))
