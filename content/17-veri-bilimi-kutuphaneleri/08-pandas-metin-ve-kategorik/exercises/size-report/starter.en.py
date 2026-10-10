import pandas as pd


def size_report(sizes):
    s = pd.Series(sizes)
    return {"sorted": s.sort_values().tolist(), "large": int((s >= "L").sum()), "max": s.max()}

result = size_report(["M", "S", "XL", "M", "L"])
print(result["sorted"])
print(result["large"], result["max"])
