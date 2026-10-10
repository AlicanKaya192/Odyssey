import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def prep_frame(rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), ["size"]),
                              ("cat", onehot, ["city"])],
                             verbose_feature_names_out=False)
    prep.set_output(transform="pandas")
    out = prep.fit_transform(df)
    return [out.columns.tolist(), float(out["size"].iloc[2])]

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
columns, size = prep_frame(ROWS)
print(*columns, sep="\n")
print(size)
