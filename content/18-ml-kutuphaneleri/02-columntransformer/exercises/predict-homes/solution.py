import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression


def predict_homes(rows, prices, new_rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    new = pd.DataFrame(new_rows, columns=["size", "city", "id"])
    prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), ["size"]),
                              ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"])])
    model = make_pipeline(prep, LinearRegression()).fit(df, prices)
    return model.predict(new).round(1).tolist()

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
print(predict_homes(ROWS, [1700, 2600, 1900, 2000], [[100.0, "Izmir", 9], [None, "Van", 10]]))
