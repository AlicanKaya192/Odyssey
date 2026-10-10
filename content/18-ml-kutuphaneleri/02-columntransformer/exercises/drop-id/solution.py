import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def keep_all_but_id(rows):
    df = pd.DataFrame(rows, columns=["size", "city", "id"])
    prep = ColumnTransformer([("drop_id", "drop", ["id"])], remainder="passthrough",
                             verbose_feature_names_out=False)
    prep.fit(df)
    return prep.get_feature_names_out().tolist()

ROWS = [[80.0, "Izmir", 1], [120.0, "Ankara", 2], [None, "Izmir", 3], [95.0, "Bursa", 4]]
print(keep_all_but_id(ROWS))
