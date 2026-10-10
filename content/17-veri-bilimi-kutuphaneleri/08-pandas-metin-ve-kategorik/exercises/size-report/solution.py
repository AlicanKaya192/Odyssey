import pandas as pd


def size_report(sizes):
    size_type = pd.CategoricalDtype(["S", "M", "L", "XL"], ordered=True)
    s = pd.Series(sizes).astype(size_type)
    return {"sorted": s.sort_values().tolist(), "large": int((s >= "L").sum()), "max": s.max()}

result = size_report(["M", "S", "XL", "M", "L"])
print(result["sorted"])
print(result["large"], result["max"])
