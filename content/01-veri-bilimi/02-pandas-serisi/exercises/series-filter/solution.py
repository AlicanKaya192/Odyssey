import pandas as pd

prices = pd.Series(
    [120, 85, 240, 60, 175],
    index=["kalem", "defter", "canta", "silgi", "kitap"],
)

expensive = prices[prices >= 100]

print(expensive)
print(expensive.size)
print(round(expensive.mean(), 1))
