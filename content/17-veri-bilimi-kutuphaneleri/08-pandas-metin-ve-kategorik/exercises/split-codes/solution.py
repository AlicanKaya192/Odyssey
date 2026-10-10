import pandas as pd


def split_codes(codes):
    pattern = r"(?P<country>[A-Z]{2})-(?P<region>\d{2})-(?P<num>\d{4})"
    parts = pd.Series(codes).str.extract(pattern).dropna()
    return {"country": parts["country"].tolist(), "num": parts["num"].astype(int).tolist()}

result = split_codes(["TR-34-0012", "TR-06-0450", "bad", "DE-11-0007"])
print(result["country"])
print(result["num"])
