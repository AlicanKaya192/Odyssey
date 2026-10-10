import pandas as pd


def tag_counts(tags):
    s = pd.Series(tags).str.split(",").explode()
    return s.value_counts().sort_index().to_dict()

print(tag_counts(["gift,fast", "fast", "gift,eco,fast"]))
