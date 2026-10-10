import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression


def predict_homes(rows, prices, new_rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    return []

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
print(predict_homes(ROWS, [1700, 2600, 1900, 2000], [[100.0, "Izmir", 9], [None, "Van", 10]]))
