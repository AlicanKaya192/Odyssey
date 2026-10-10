import pandas as pd
from sklearn.preprocessing import OrdinalEncoder


def encode_sizes(sizes):
    df = pd.DataFrame({"size": sizes})
    return OrdinalEncoder().fit_transform(df).ravel().astype(int).tolist()

print(encode_sizes(["M", "S", "XL", "L", "S"]))
