import pandas as pd


def split_codes(codes):
    parts = pd.Series(codes).str.split("-", expand=True)
    return {"country": parts[0].tolist(), "num": parts[2].tolist()}

result = split_codes(["TR-34-0012", "TR-06-0450", "bad", "DE-11-0007"])
print(result["country"])
print(result["num"])
