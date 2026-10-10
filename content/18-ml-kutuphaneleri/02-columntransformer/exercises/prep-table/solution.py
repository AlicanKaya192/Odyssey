import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def prep_table(rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    onehot = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    prep = ColumnTransformer([("num", numeric, ["size"]), ("cat", onehot, ["city"])])
    out = prep.fit_transform(df)
    return [list(out.shape), prep.get_feature_names_out().tolist()]

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
shape, names = prep_table(ROWS)
print(shape)
print(*names, sep="\n")
