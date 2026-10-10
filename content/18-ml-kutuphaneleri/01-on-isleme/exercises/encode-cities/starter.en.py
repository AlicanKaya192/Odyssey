import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_cities(train, test):
    enc = OneHotEncoder(sparse_output=False).fit(pd.DataFrame({"city": train}))
    coded = enc.transform(pd.DataFrame({"city": test})).astype(int).tolist()
    return {"names": enc.get_feature_names_out().tolist(), "test": coded}

result = encode_cities(["Izmir", "Ankara", "Izmir", "Bursa"], ["Van", "Bursa"])
print(result["names"])
print(result["test"])
